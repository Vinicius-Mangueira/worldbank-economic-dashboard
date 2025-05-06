# backend/app.py

from fastapi import FastAPI, HTTPException, Query
from typing import List
import uvicorn
from data_loader import (
    get_countries_df,
    get_indicators_df,
    get_indicator_data_df,
    forecast_indicator  # se existir; caso contrário, implemente depois
)

app = FastAPI(
    title="World Bank Economic Dashboard API",
    description="API para fornecer dados e previsões de indicadores econômicos via World Bank",
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
    country: str = Query(..., description="Código do país (ex: BR)"),
    indicator: str = Query(..., description="Código do indicador (ex: NY.GDP.MKTP.CD)"),
    start: int = Query(..., description="Ano inicial (ex: 2000)"),
    end: int = Query(..., description="Ano final (ex: 2022)")
):
    try:
        df = get_indicator_data_df(country, indicator, start, end)
        return df.to_dict(orient="records")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Se você já tiver forecasting implementado em data_loader:
@app.get("/forecast", response_model=List[dict])
async def forecast(
    country: str = Query(..., description="Código do país (ex: BR)"),
    indicator: str = Query(..., description="Código do indicador (ex: NY.GDP.MKTP.CD)"),
    years_ahead: int = Query(5, description="Número de anos à frente para previsão")
):
    try:
        df_forecast = forecast_indicator(country, indicator, years_ahead)
        return df_forecast.to_dict(orient="records")
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Forecast ainda não implementado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
    # Para rodar o servidor, use o comando:
    # uvicorn backend.app:app --host