# backend/data_loader.py
"""
Module for loading and transforming World Bank economic indicator data.
Functions:
- get_countries_df(): returns DataFrame of country codes and names
- get_indicators_df(): returns DataFrame of indicator codes and names
- get_indicator_data_df(country, indicator, start, end): returns time series DataFrame
- forecast_indicator(country, indicator, years_ahead): forecasts future values
"""
import requests
import pandas as pd
from typing import List, Tuple
from io import StringIO

# For forecasting
from statsmodels.tsa.arima.model import ARIMA

WB_API_BASE = "http://api.worldbank.org/v2"


def get_countries_df() -> pd.DataFrame:
    """
    Fetch list of countries from World Bank API.
    Returns DataFrame with columns: ['id', 'name', 'region', 'capitalCity']
    """
    url = f"{WB_API_BASE}/country?format=json&per_page=500"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()[1]
    df = pd.json_normalize(data)
    return df[['id', 'name', 'region.value', 'capitalCity']].rename(
        columns={'region.value': 'region'}
    )


def get_indicators_df() -> pd.DataFrame:
    """
    Fetch list of all indicators.
    Returns DataFrame with columns: ['id', 'name', 'sourceNote']
    """
    url = f"{WB_API_BASE}/indicator?format=json&per_page=20000"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()[1]
    df = pd.json_normalize(data)
    return df[['id', 'name', 'sourceNote']]


def get_indicator_data_df(country: str, indicator: str, start: int, end: int) -> pd.DataFrame:
    """
    Fetch time series for a given country and indicator between start and end years.
    Returns DataFrame with columns ['country', 'indicator', 'year', 'value'] sorted by year.
    """
    url = (
        f"{WB_API_BASE}/country/{country}/indicator/{indicator}"
        f"?date={start}:{end}&format=json&per_page=1000"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    json_data = resp.json()
    if not json_data or len(json_data) < 2:
        raise ValueError(f"No data returned for {country} {indicator}")
    records = json_data[1]
    df = pd.json_normalize(records)
    df = df[['country.value', 'indicator.id', 'date', 'value']]
    df.columns = ['country', 'indicator', 'year', 'value']
    df['year'] = df['year'].astype(int)
    df = df.sort_values('year').reset_index(drop=True)
    return df


def forecast_indicator(country: str, indicator: str, years_ahead: int) -> pd.DataFrame:
    """
    Forecast future indicator values using ARIMA model.
    Returns DataFrame with historical and forecasted values:
    ['country', 'indicator', 'year', 'value', 'forecast']
    """
    # Fetch historical data
    hist = get_indicator_data_df(country, indicator, 1960, pd.Timestamp.now().year)
    series = hist.set_index('year')['value'].dropna()
    if len(series) < 10:
        raise ValueError("Not enough data points to fit ARIMA model")
    # Fit ARIMA
    model = ARIMA(series, order=(1,1,1))
    fitted = model.fit()
    # Forecast
    forecast_res = fitted.forecast(steps=years_ahead)
    # Build forecast DF
    last_year = series.index.max()
    forecast_years = list(range(last_year + 1, last_year + years_ahead + 1))
    df_forecast = pd.DataFrame({
        'country': country,
        'indicator': indicator,
        'year': forecast_years,
        'forecast': forecast_res.values
    })
    # Merge with historical
    hist = hist.rename(columns={'value': 'actual'})
    merged = pd.concat([
        hist[['country', 'indicator', 'year', 'actual']],
        df_forecast
    ], sort=False).reset_index(drop=True)
    # Fill missing forecast in historical and vice versa
    merged['value'] = merged['forecast'].fillna(merged['actual'])
    merged = merged[['country', 'indicator', 'year', 'value']]
    return merged
