# File: backend/app.py
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Tuple
from backend.data_loader import (
    get_countries_df,
    get_indicators_df,
    get_indicator_data_df,
    forecast_indicator
)
import uvicorn

app = FastAPI(
    title="World Bank Economic Dashboard API",
    version="1.0.0"
)

# Caches to store preloaded data
_indicators_cache: Optional[List[dict]] = None
_countries_cache: Optional[List[dict]] = None

@app.on_event("startup")
async def load_caches():
    """
    Preload countries and indicators once at startup
    to serve quickly from memory.
    """
    global _indicators_cache, _countries_cache
    try:
        # Load and cache indicators
        df_ind = get_indicators_df()
        _indicators_cache = df_ind.to_dict(orient="records")
        # Load and cache countries
        df_countries = get_countries_df()
        _countries_cache = df_countries.to_dict(orient="records")
        print(f"Cache loaded: {_countries_cache.__len__()} countries and {_indicators_cache.__len__()} indicators")
    except Exception as e:
        # Log but do not crash startup
        print(f"Error preloading cache: {e}")

@app.get("/countries", response_model=List[dict])
def countries():
    """Return the list of countries, cached if available."""
    if _countries_cache is not None:
        return _countries_cache
    try:
        df = get_countries_df()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indicators", response_model=List[dict])
def indicators():
    """Return the list of indicators, cached if available."""
    if _indicators_cache is not None:
        return _indicators_cache
    try:
        df = get_indicators_df()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data", response_model=List[dict])
def data(
    country: str = Query(..., description="ISO3 country code"),
    indicator: str = Query(..., description="Indicator code"),
    start: int = Query(2000, description="Start year"),
    end: int = Query(2022, description="End year")
):
    """Return time series data for a given country and indicator."""
    try:
        df = get_indicator_data_df(country, indicator, start, end)
        return df.to_dict(orient="records")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/forecast", response_model=List[dict])
def forecast(
    country: str = Query(..., description="ISO3 country code"),
    indicator: str = Query(..., description="Indicator code"),
    start: int = Query(1960, description="Start year for historical fit"),
    end: Optional[int] = Query(None, description="End year for historical fit"),
    years_ahead: int = Query(5, description="Years to forecast ahead"),
    arima_order: Optional[Tuple[int,int,int]] = Query((1,1,1), description="ARIMA order parameters (p,d,q)")
):
    """Return forecast data based on ARIMA model for a given country and indicator."""
    try:
        from datetime import datetime
        if end is None:
            end = datetime.now().year
        df_fc = forecast_indicator(country, indicator, start, end, years_ahead, arima_order)
        return df_fc.to_dict(orient="records")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run with: uvicorn backend.app:app
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
