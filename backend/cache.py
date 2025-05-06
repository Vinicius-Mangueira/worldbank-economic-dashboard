# cache.py
import sqlite3
import pandas as pd
from typing import Optional

DB_PATH = "worldbank.db"


def get_connection(path: str = DB_PATH):
    """
    Retorna conexão SQLite (thread-safe).
    """
    conn = sqlite3.connect(path, check_same_thread=False)
    return conn


def init_db(conn: sqlite3.Connection):
    """
    Cria tabela de cache se não existir.
    """
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS indicator_data (
                country TEXT,
                indicator TEXT,
                year INTEGER,
                value REAL,
                PRIMARY KEY (country, indicator, year)
            )
            """
        )


def fetch_indicator(
    conn: sqlite3.Connection,
    country: str,
    indicator: str,
    start: int,
    end: int
) -> pd.DataFrame:
    """
    Tenta ler série histórica do cache.
    Retorna DataFrame com colunas ['year', 'value'].
    """
    sql = (
        "SELECT year, value"
        " FROM indicator_data"
        " WHERE country=? AND indicator=? AND year BETWEEN ? AND ?"
        " ORDER BY year"
    )
    df = pd.read_sql_query(sql, conn, params=(country, indicator, start, end))
    return df


def store_indicator(
    conn: sqlite3.Connection,
    df: pd.DataFrame
):
    """
    Armazena DataFrame no cache.
    Espera colunas ['country', 'indicator', 'year', 'value'].
    """
    df.to_sql("indicator_data", conn, if_exists="append", index=False)