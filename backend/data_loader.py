
# File: backend/data_loader.py
import logging
import requests
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WB_API_BASE = "http://api.worldbank.org/v2"
# Reusar sessão HTTP para performance e timeouts
_session = requests.Session()
_session.headers.update({"User-Agent": "worldbank-client/1.0"})
_DEFAULT_TIMEOUT = 10  # segundos


def _fetch_all(path: str, params: dict) -> list:
    """
    Busca todos os registros paginados da API do World Bank.
    """
    records = []
    page = 1
    while True:
        params.update({"format": "json", "per_page": 1000, "page": page})
        url = f"{WB_API_BASE}/{path}"
        try:
            resp = _session.get(url, params=params, timeout=_DEFAULT_TIMEOUT)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao chamar {url}: {e}")
            raise ValueError(f"Erro de requisição à API do Banco Mundial: {e}")

        data = resp.json()
        if not data or len(data) < 2:
            logger.error(f"Resposta inesperada da API: {data}")
            raise ValueError("Resposta inválida da API do Banco Mundial.")

        meta, page_data = data[0], data[1]
        records.extend(page_data)
        total_pages = meta.get("pages", 0)
        if page >= total_pages:
            break
        page += 1
    logger.info(f"Fetched {len(records)} records from {path}")
    return records


def get_countries_df() -> pd.DataFrame:
    """
    Busca lista de países disponíveis no World Bank.
    Retorna DataFrame com colunas ['id','name','region','capitalCity']
    """
    raw = _fetch_all("country", {})
    df = pd.json_normalize(raw)
    required_cols = ['id', 'name', 'region.value', 'capitalCity']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Campo esperado não encontrado: {col}")
    logger.info("Countries dataframe built with %d rows", len(df))
    return df[required_cols]


def get_indicators_df() -> pd.DataFrame:
    """
    Busca lista de indicadores.
    Retorna DataFrame com colunas ['id','name']
    """
    raw = _fetch_all("indicator", {})
    df = pd.json_normalize(raw)
    required_cols = ['id', 'name']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Campo esperado não encontrado: {col}")
    logger.info("Indicators dataframe built with %d rows", len(df))
    return df[required_cols]


def get_indicator_data_df(country: str, indicator: str, start: int, end: int) -> pd.DataFrame:
    """
    Busca série histórica de um indicador para um país entre start e end.
    Retorna DataFrame com colunas ['country','indicator','year','value']
    """
    if start > end:
        raise ValueError("Ano inicial não pode ser maior que ano final.")
    path = f"country/{country}/indicator/{indicator}"
    raw = _fetch_all(path, {"date": f"{start}:{end}"})
    df = pd.json_normalize(raw)
    expected = ['country.value', 'indicator.id', 'date', 'value']
    for col in expected:
        if col not in df.columns:
            raise ValueError(f"Campo esperado não encontrado: {col}")
    df = df[expected]
    df.columns = ['country', 'indicator', 'year', 'value']
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['year', 'value'])
    df = df.sort_values('year').reset_index(drop=True)
    if df.empty:
        raise ValueError(f"Nenhum dado encontrado para {country}-{indicator} de {start} a {end}.")
    logger.info("Data for %s - %s from %d to %d: %d records", country, indicator, start, end, len(df))
    return df


def forecast_indicator(country: str, indicator: str, start: int, end: int,
                       years_ahead: int, arima_order: tuple = (1, 1, 1)) -> pd.DataFrame:
    """
    Ajusta ARIMA à série histórica e prevê anos à frente.
    Retorna DataFrame com colunas ['country','indicator','year','value'] incluindo forecast.
    """
    hist_df = get_indicator_data_df(country, indicator, start, end)
    series = hist_df.set_index('year')['value']
    if len(series) < 10:
        message = f"Série muito curta ({len(series)} pontos); mínimo 10 pontos para ARIMA."
        logger.error(message)
        raise ValueError(message)
    logger.info("Fitting ARIMA(order=%s) for %s-%s", arima_order, country, indicator)
    model = ARIMA(series, order=arima_order)
    fitted = model.fit()
    forecast_vals = fitted.forecast(steps=years_ahead)
    last_year = int(series.index.max())
    fc_years = list(range(last_year + 1, last_year + years_ahead + 1))
    df_fc = pd.DataFrame({
        'country': country,
        'indicator': indicator,
        'year': fc_years,
        'value': forecast_vals.values
    })
    result = pd.concat([hist_df, df_fc], ignore_index=True)
    logger.info("Forecast generated for %d future years", years_ahead)
    return result[['country', 'indicator', 'year', 'value']]

