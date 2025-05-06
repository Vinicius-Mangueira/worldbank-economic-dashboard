
# backend/app.py
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Tuple
from data_loader import (
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

@app.get("/countries", response_model=List[dict])
def countries():
    try:
        df = get_countries_df()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indicators", response_model=List[dict])
def indicators():
    try:
        df = get_indicators_df()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data", response_model=List[dict])
def data(
    country: str = Query(...),
    indicator: str = Query(...),
    start: int = Query(2000),
    end: int = Query(2022)
):
    try:
        df = get_indicator_data_df(country, indicator, start, end)
        return df.to_dict(orient="records")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/forecast", response_model=List[dict])
def forecast(
    country: str = Query(...),
    indicator: str = Query(...),
    start: int = Query(1960),
    end: Optional[int] = Query(None),
    years_ahead: int = Query(5),
    arima_order: Optional[Tuple[int,int,int]] = Query((1,1,1))
):
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
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
