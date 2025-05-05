import requests
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List

# Base URL for World Bank API
BASE_URL = "http://api.worldbank.org/v2"

# Path to local SQLite database file
db_path = Path(__file__).parent.parent / "database" / "dataset.db"


def init_db():
    """
    Initializes the SQLite database and creates required tables if they do not exist.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create countries table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        id TEXT PRIMARY KEY,
        name TEXT,
        region TEXT,
        incomeLevel TEXT,
        capitalCity TEXT
    )
    """)

    # Create indicators table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS indicators (
        id TEXT PRIMARY KEY,
        name TEXT,
        sourceNote TEXT
    )
    """)

    # Create indicator_data table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS indicator_data (
        country TEXT,
        indicator TEXT,
        year INTEGER,
        value REAL,
        PRIMARY KEY (country, indicator, year),
        FOREIGN KEY(country) REFERENCES countries(id),
        FOREIGN KEY(indicator) REFERENCES indicators(id)
    )
    """)

    conn.commit()
    conn.close()


def save_df_to_sqlite(df: pd.DataFrame, table_name: str, if_exists: str = "append"):
    """
    Saves a pandas DataFrame to the specified SQLite table.

    Args:
        df: DataFrame to save.
        table_name: Name of the table in SQLite.
        if_exists: Behavior if the table exists ("fail", "replace", "append").
    """
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    conn.close()


def get_countries_df(format: str = "json") -> pd.DataFrame:
    # Returns a DataFrame with countries supported by the World Bank API
    url = f"{BASE_URL}/country"
    params = {"format": format, "per_page": 300}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()[1]
    df = pd.DataFrame(data)
    return df


def get_indicators_df(format: str = "json", per_page: int = 2000) -> pd.DataFrame:
    # Returns a DataFrame with available indicators
    url = f"{BASE_URL}/indicator"
    params = {"format": format, "per_page": per_page}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()[1]
    df = pd.DataFrame(data)
    return df


def get_indicator_data_df(
    country_code: str,
    indicator_code: str,
    date_from: Optional[int] = None,
    date_to: Optional[int] = None,
    format: str = "json"
) -> pd.DataFrame:
    # Returns a DataFrame with time series data for a given indicator and country
    url = f"{BASE_URL}/country/{country_code}/indicator/{indicator_code}"
    params: Dict[str, Any] = {"format": format, "per_page": 1000}
    if date_from is not None:
        params["date"] = f"{date_from}:{date_to or ''}"
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()[1]
    df = pd.DataFrame(data)
    df = df[["country", "date", "value", "indicator"]]
    df["country"] = df["country"].apply(lambda x: x["id"])
    df["indicator"] = df["indicator"].apply(lambda x: x["id"])
    df = df.rename(columns={"date": "year", "value": "indicator_value"})
    df["year"] = df["year"].astype(int)
    return df.sort_values(by="year")


def get_multiple_indicators_df(
    country_code: str,
    indicators: List[str],
    date_from: Optional[int] = None,
    date_to: Optional[int] = None,
    format: str = "json"
) -> pd.DataFrame:
    # Combines multiple indicators for a country into one DataFrame
    dfs: List[pd.DataFrame] = []
    for ind in indicators:
        df = get_indicator_data_df(country_code, ind, date_from, date_to, format)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


if __name__ == "__main__":
    # Initialize database and tables
    init_db()

    # Load and save countries
    countries_df = get_countries_df()
    save_df_to_sqlite(countries_df, "countries", if_exists="replace")

    # Load and save indicators
    indicators_df = get_indicators_df()
    save_df_to_sqlite(indicators_df, "indicators", if_exists="replace")

    # Example: Load and save GDP data for Brazil (2000-2020)
    gdp_df = get_indicator_data_df("BRA", "NY.GDP.MKTP.CD", 2000, 2020)
    save_df_to_sqlite(gdp_df, "indicator_data")

    # Example: Load and save multiple indicators
    indicators_list = ["NY.GDP.MKTP.CD", "FP.CPI.TOTL.ZG"]
    multi_df = get_multiple_indicators_df("BRA", indicators_list, 2010, 2020)
    save_df_to_sqlite(multi_df, "indicator_data")
