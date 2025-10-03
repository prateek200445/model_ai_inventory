from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import model

app = FastAPI(title="Inventory Forecast API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[model.VERCEL_FRONTEND],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ForecastRequest(BaseModel):
    days: int = 7
    product_id: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    min_rating: Optional[float] = None
    max_price: Optional[float] = None
    min_discount: Optional[float] = None

@app.get("/")
async def root():
    return {"status": "Inventory Forecast API is running"}

@app.post("/forecast")
async def get_forecast(request: ForecastRequest):
    try:
        result = model.forecast(
            days=request.days,
            product_id=request.product_id,
            category=request.category,
            region=request.region,
            min_rating=request.min_rating,
            max_price=request.max_price,
            min_discount=request.min_discount
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/plot")
async def get_plot():
    try:
        return FileResponse("forecast_plot.png")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Plot not found")