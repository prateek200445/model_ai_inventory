from fastapi import FastAPI, HTTPException
from tariff_impact_model import TariffImpactModel
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Tariff Impact Analysis API", version="1.0.0")
model = TariffImpactModel()

# Add API information
@app.on_event("startup")
async def startup_event():
    print("Starting Tariff Impact Analysis API on port 8001")

class TariffRequest(BaseModel):
    product_id: Optional[str] = None
    category: Optional[str] = None
    tariff_percentage: float

@app.post("/analyze-tariff")
async def analyze_tariff_impact(request: TariffRequest):
    try:
        result = model.analyze_tariff_impact(
            product_id=request.product_id,
            category=request.category,
            tariff_percentage=request.tariff_percentage
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Tariff Impact Analysis API"}