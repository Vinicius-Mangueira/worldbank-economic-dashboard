# backend/data_loader.py
"""
Module para carregamento e transformação de dados de indicadores econômicos da World Bank.
Funções:
- get_countries_df(): retorna DataFrame com países
- get_indicators_df(): retorna DataFrame com indicadores
- get_indicator_data_df(country, indicator, start, end): retorna série histórica
- forecast_indicator(country, indicator, start, end, years_ahead, arima_order): faz previsão ARIMA
"""
import requests
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

WB_API_BASE = "http://api.worldbank.org/v2"


def get_countries_df() -> pd.DataFrame:
    """
    Busca lista de países disponíveis no World Bank.
    Retorna DataFrame com colunas ['id','name','region','capitalCity']
    """
    url = f"{WB_API_BASE}/country?format=json&per_page=500"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()[1]
    df = pd.json_normalize(data)
    return df[['id','name','region.value','capitalCity']].rename(columns={'region.value':'region'})


def get_indicators_df() -> pd.DataFrame:
    """
    Busca lista de indicadores.
    Retorna DataFrame com colunas ['id','name']
    """
    url = f"{WB_API_BASE}/indicator?format=json&per_page=1000"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()[1]
    df = pd.json_normalize(data)
    return df[['id','name']]


def get_indicator_data_df(country: str, indicator: str, start: int, end: int) -> pd.DataFrame:
    """
    Busca série histórica de um indicador para um país entre start e end.
    Retorna DataFrame com colunas ['country','indicator','year','value']
    """
    url = (
        f"{WB_API_BASE}/country/{country}/indicator/{indicator}"
        f"?date={start}:{end}&format=json&per_page=1000"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    raw = resp.json()[1]
    df = pd.json_normalize(raw)
    df = df[['country.value','indicator.id','date','value']]
    df.columns = ['country','indicator','year','value']
    df['year'] = df['year'].astype(int)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df.dropna(subset=['value']).sort_values('year').reset_index(drop=True)


def forecast_indicator(country: str, indicator: str, start: int, end: int,
                       years_ahead: int, arima_order: tuple = (1,1,1)) -> pd.DataFrame:
    """
    Ajusta ARIMA à série histórica e prevê anos à frente.
    Retorna DataFrame com colunas ['country','indicator','year','value'] incluindo forecast.
    """
    hist_df = get_indicator_data_df(country, indicator, start, end)
    series = hist_df.set_index('year')['value']
    if len(series) < 10:
        raise ValueError("Série muito curta para ARIMA (mínimo 10 pontos).")
    model = ARIMA(series, order=arima_order)
    fitted = model.fit()
    forecast_vals = fitted.forecast(steps=years_ahead)
    last_year = series.index.max()
    fc_years = list(range(last_year+1, last_year+years_ahead+1))
    df_fc = pd.DataFrame({
        'country': country,
        'indicator': indicator,
        'year': fc_years,
        'value': forecast_vals.values
    })
    return pd.concat([hist_df, df_fc], ignore_index=True)[['country','indicator','year','value']]
