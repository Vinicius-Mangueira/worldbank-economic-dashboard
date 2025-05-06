# backend/app.py

from fastapi import FastAPI, HTTPException, Query
from typing import List
import uvicorn
from .data_loader import (
    get_countries_df,
    get_indicators_df,
    get_indicator_data_df,
    forecast_indicator  # If not implemented, should raise NotImplementedError
)

app = FastAPI(
    title="World Bank Economic Dashboard API",
    description="API to provide economic indicator data and forecasts via the World Bank",
    version="1.0.0"
)

@app.get("/countries", response_model=List[dict])
async def countries():
    try:
        df = get_countries_df()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indicators", response_model=List[dict])
async def indicators():
    try:
        df = get_indicators_df()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data", response_model=List[dict])
async def data(
    country: str = Query(..., description="Country code (e.g., BR)"),
    indicator: str = Query(..., description="Indicator code (e.g., NY.GDP.MKTP.CD)"),
    start: int = Query(..., description="Start year (e.g., 2000)"),
    end: int = Query(..., description="End year (e.g., 2022)")
):
    try:
        df = get_indicator_data_df(country, indicator, start, end)
        return df.to_dict(orient="records")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/forecast", response_model=List[dict])
async def forecast(
    country: str = Query(..., description="Country code (e.g., BR)"),
    indicator: str = Query(..., description="Indicator code (e.g., NY.GDP.MKTP.CD)"),
    years_ahead: int = Query(5, description="Years ahead to forecast")
):
    try:
        df_forecast = forecast_indicator(country, indicator, years_ahead)
        return df_forecast.to_dict(orient="records")
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Forecast not implemented yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run directly: python backend/app.py
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
