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
            raise

        data = resp.json()
        # data[0] contém metadados, data[1] os registros
        meta, page_data = data[0], data[1]
        records.extend(page_data)
        if page >= meta.get("pages", 0):
            break
        page += 1
    return records


def get_countries_df() -> pd.DataFrame:
    """
    Busca lista de países disponíveis no World Bank.
    Retorna DataFrame com colunas ['id','name','region','capitalCity']
    """
    raw = _fetch_all("country", {})
    df = pd.json_normalize(raw)
    return df[['id', 'name', 'region.value', 'capitalCity']]


def get_indicators_df() -> pd.DataFrame:
    """
    Busca lista de indicadores.
    Retorna DataFrame com colunas ['id','name']
    """
    raw = _fetch_all("indicator", {})
    df = pd.json_normalize(raw)
    return df[['id', 'name']]


def get_indicator_data_df(country: str, indicator: str, start: int, end: int) -> pd.DataFrame:
    """
    Busca série histórica de um indicador para um país entre start e end.
    Retorna DataFrame com colunas ['country','indicator','year','value']
    """
    path = f"country/{country}/indicator/{indicator}"
    raw = _fetch_all(path, {"date": f"{start}:{end}"})
    df = pd.json_normalize(raw)
    df = df[['country.value', 'indicator.id', 'date', 'value']]
    df.columns = ['country', 'indicator', 'year', 'value']
    df['year'] = df['year'].astype(int)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df.dropna(subset=['value']).sort_values('year').reset_index(drop=True)


def forecast_indicator(country: str, indicator: str, start: int, end: int,
                       years_ahead: int, arima_order: tuple = (1, 1, 1)) -> pd.DataFrame:
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
    fc_years = list(range(last_year + 1, last_year + years_ahead + 1))
    df_fc = pd.DataFrame({
        'country': country,
        'indicator': indicator,
        'year': fc_years,
        'value': forecast_vals.values
    })
    return pd.concat([hist_df, df_fc], ignore_index=True)[['country', 'indicator', 'year', 'value']]

