import requests
from typing import Optional, Dict, Any, List

BASE_URL = "http://api.worldbank.org/v2"

def get_countries(format: str = "json") -> List[Dict[str, Any]]:
    # Returns the list of countries supported by the World Bank API
    url = f"{BASE_URL}/country"
    params = {
        "format": format,
        "per_page": 300  # get all countries in one request
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data[1]  # second element contains the actual list


def get_indicators(format: str = "json", per_page: int = 2000) -> List[Dict[str, Any]]:
    # Returns the list of available indicators from the World Bank API
    url = f"{BASE_URL}/indicator"
    params = {
        "format": format,
        "per_page": per_page
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data[1]


def get_indicator_data(
    country_code: str,
    indicator_code: str,
    date_from: Optional[int] = None,
    date_to: Optional[int] = None,
    format: str = "json"
) -> List[Dict[str, Any]]:
    # Fetches time series data for a given indicator and country
    url = f"{BASE_URL}/country/{country_code}/indicator/{indicator_code}"
    params: Dict[str, Any] = {
        "format": format,
        "per_page": 1000
    }
    if date_from is not None:
        params["date"] = f"{date_from}:{date_to or ''}"
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data[1]


def get_multiple_indicators(
    country_code: str,
    indicators: List[str],
    date_from: Optional[int] = None,
    date_to: Optional[int] = None,
    format: str = "json"
) -> Dict[str, List[Dict[str, Any]]]:
    # Fetches multiple indicators for the same country and time range
    result = {}
    for ind in indicators:
        result[ind] = get_indicator_data(country_code, ind, date_from, date_to, format)
    return result


# Example usage
if __name__ == "__main__":
    # List countries
    countries = get_countries()
    print(f"Total countries: {len(countries)}")
    print(countries[0])

    # Fetch GDP for Brazil from 2000 to 2020
    gdp_data = get_indicator_data("BRA", "NY.GDP.MKTP.CD", date_from=2000, date_to=2020)
    for entry in gdp_data[:5]:
        print(entry["date"], entry["value"])

    # Fetch multiple indicators for Brazil
    indicators = ["NY.GDP.MKTP.CD", "FP.CPI.TOTL.ZG"]  # GDP and inflation
    multi = get_multiple_indicators("BRA", indicators, date_from=2010, date_to=2020)
    print(multi["FP.CPI.TOTL.ZG"][:3])
