
# crud.py
import pandas as pd
from typing import List
from data_loader import get_countries_df, get_indicators_df, get_indicator_data_df
import cache

# inicializa cache
_conn = cache.get_connection()
cache.init_db(_conn)


def get_countries() -> List[str]:
    df = get_countries_df()
    return sorted(df['id'].tolist())


def get_indicators() -> List[str]:
    df = get_indicators_df()
    return sorted(df['id'].tolist())


def get_indicator_data(
    country: str,
    indicator: str,
    start: int,
    end: int
) -> pd.DataFrame:
    """
    Tenta primeiro ler do cache. Em caso de cache miss, busca na API e armazena.
    """
    df_cache = cache.fetch_indicator(_conn, country, indicator, start, end)
    if not df_cache.empty:
        return df_cache

    # cache miss: busca na API
    df_api = get_indicator_data_df(country, indicator, start, end)
    if not df_api.empty:
        # prepara DataFrame para armazenamento
        df_to_store = df_api.copy()
        df_to_store['country'] = country
        df_to_store['indicator'] = indicator
        cache.store_indicator(_conn, df_to_store)
    return df_api


def get_normalized_indicator_data(
    country: str,
    indicator: str,
    start: int,
    end: int
) -> pd.DataFrame:
    """
    Retorna DataFrame com colunas ['year', 'normalized'] (value/1e6).
    """
    df = get_indicator_data(country, indicator, start, end)
    df['normalized'] = df['value'] / 1e6
    return df[['year', 'normalized']]
