
# File: backend/app.py
import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Tuple
from backend.data_loader import (
    get_countries_df,
    get_indicators_df,
    get_indicator_data_df,
    forecast_indicator
)
import uvicorn

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="World Bank Economic Dashboard API",
    version="1.0.0"
)

# Caches with simple TTL
_indicators_cache: Optional[List[dict]] = None
_countries_cache: Optional[List[dict]] = None
_cache_timestamp: Optional[float] = None
_CACHE_TTL = 3600  # segundos

@app.on_event("startup")
async def load_caches():
    """
    Preload countries and indicators once at startup
    and refresh caches when TTL expires.
    """
    await _refresh_caches()

async def _refresh_caches():
    import time
    global _indicators_cache, _countries_cache, _cache_timestamp
    try:
        logger.info("Refreshing caches...")
        df_ind = get_indicators_df()
        _indicators_cache = df_ind.to_dict(orient="records")
        df_countries = get_countries_df()
        _countries_cache = df_countries.to_dict(orient="records")
        _cache_timestamp = time.time()
        logger.info(f"Cache loaded: {len(_countries_cache)} countries and {len(_indicators_cache)} indicators")
    except Exception as e:
        logger.error(f"Error preloading cache: {e}")
        # propagate or decide fallback

def _ensure_cache_valid():
    import time
    if _cache_timestamp is None or (time.time() - _cache_timestamp) > _CACHE_TTL:
        import asyncio
        asyncio.run(_refresh_caches())

@app.get("/countries", response_model=List[dict])
def countries():
    """Return the list of countries, cached if available."""
    try:
        _ensure_cache_valid()
        return _countries_cache or []
    except Exception as e:
        logger.exception("Failed to fetch countries cache")
        raise HTTPException(status_code=500, detail="Erro ao obter lista de países.")

@app.get("/indicators", response_model=List[dict])
def indicators():
    """Return the list of indicators, cached if available."""
    try:
        _ensure_cache_valid()
        return _indicators_cache or []
    except Exception as e:
        logger.exception("Failed to fetch indicators cache")
        raise HTTPException(status_code=500, detail="Erro ao obter lista de indicadores.")

@app.get("/data", response_model=List[dict])
def data(
    country: str = Query(..., min_length=3, max_length=3, description="ISO3 country code"),
    indicator: str = Query(..., min_length=1, description="Indicator code"),
    start: int = Query(2000, ge=1900, le=2100, description="Start year"),
    end: int = Query(2022, ge=1900, le=2100, description="End year")
):
    """Return time series data for a given country and indicator."""
    if start > end:
        raise HTTPException(status_code=400, detail="Ano inicial não pode ser maior que ano final.")
    try:
        df = get_indicator_data_df(country, indicator, start, end)
        if df.empty:
            raise HTTPException(status_code=404, detail="Dados não encontrados para os parâmetros informados.")
        return df.to_dict(orient="records")
    except HTTPException:
        raise
    except ValueError as ve:
        logger.warning(f"ValueError in /data: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception("Unexpected error in /data")
        raise HTTPException(status_code=500, detail="Erro interno ao processar dados.")

@app.get("/forecast", response_model=List[dict])
def forecast(
    country: str = Query(..., min_length=3, max_length=3, description="ISO3 country code"),
    indicator: str = Query(..., min_length=1, description="Indicator code"),
    start: int = Query(1960, ge=1900, le=2100, description="Start year for fit"),
    end: Optional[int] = Query(None, ge=1900, le=2100, description="End year for fit"),
    years_ahead: int = Query(5, ge=1, le=50, description="Years to forecast ahead"),
    arima_order: Optional[Tuple[int,int,int]] = Query((1,1,1), description="ARIMA order parameters (p,d,q)")
):
    """Return forecast data based on ARIMA model for a given country and indicator."""
    try:
        from datetime import datetime
        if end is None:
            end = datetime.now().year
        if start > end:
            raise HTTPException(status_code=400, detail="Ano inicial não pode ser maior que ano final.")
        df_fc = forecast_indicator(country, indicator, start, end, years_ahead, arima_order)
        return df_fc.to_dict(orient="records")
    except HTTPException:
        raise
    except ValueError as ve:
        logger.warning(f"ValueError in /forecast: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception("Unexpected error in /forecast")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar previsão.")

if __name__ == "__main__":
    # Run with: uvicorn backend.app:app --reload
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)

