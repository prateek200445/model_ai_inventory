# api.py
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import model   # <-- make sure model.py is in same folder
import base64  # for encoding the image

app = FastAPI(title="Inventory Forecast API", version="1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[model.VERCEL_FRONTEND],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )

# Input schema (if you want parameters from frontend)
class ForecastRequest(BaseModel):
    days: int = 7   # default forecast horizon
    product_id: str | None = None  # optional product filter
    category: str | None = None    # optional category filter
    region: str | None = None      # optional region filter
    min_rating: float | None = None  # optional minimum rating filter
    max_price: float | None = None   # optional maximum price filter
    min_discount: float | None = None  # optional minimum discount filter

    class Config:
        json_schema_extra = {
            "example": {
                "days": 7,
                "product_id": None,
                "category": None,
                "region": None,
                "min_rating": None,
                "max_price": None,
                "min_discount": None
            }
        }


@app.get("/")
def home():
    return {"message": "Inventory Forecast API is running 🚀"}

@app.get("/plot")
async def get_plot():
    """Get the latest generated forecast plot"""
    return FileResponse("forecast_plot.png", media_type="image/png")


@app.get("/forecast")
async def get_forecast(
    days: int = 7,
    product_id: str | None = None,
    category: str | None = None,
    region: str | None = None,
    min_rating: float | None = None,
    max_price: float | None = None,
    min_discount: float | None = None
):
    # Call your model's forecast function with all parameters
    result = model.forecast(
        days=days,
        product_id=product_id,
        category=category,
        region=region,
        min_rating=min_rating,
        max_price=max_price,
        min_discount=min_discount
    )

    # Read and encode the plot image
    try:
        with open("forecast_plot.png", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        encoded_image = None

    response = {
        "Reorder Point": result["Reorder Point"],
        "Safety Stock": result["Safety Stock"],
        "Minimum Level": result["Minimum Level"],
        "Maximum Level": result["Maximum Level"],
        "Forecast": result["Forecast"],   # dictionary {date: demand}
        "Warnings": result["Warnings"],   # list of warnings
        "plot_data": {
            "image": encoded_image,
            "content_type": "image/png",
            "encoding": "base64"
        }
    }
    return response

@app.post("/forecast")
def post_forecast(request: ForecastRequest):
    # Call your model's forecast function with all parameters
    result = model.forecast(
        days=request.days,
        product_id=request.product_id,
        category=request.category,
        region=request.region,
        min_rating=request.min_rating,
        max_price=request.max_price,
        min_discount=request.min_discount
    )

    # Read and encode the plot image
    try:
        with open("forecast_plot.png", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        encoded_image = None

    response = {
        "Reorder Point": result["Reorder Point"],
        "Safety Stock": result["Safety Stock"],
        "Minimum Level": result["Minimum Level"],
        "Maximum Level": result["Maximum Level"],
        "Forecast": result["Forecast"],   # dictionary {date: demand}
        "Warnings": result["Warnings"],   # list of warnings
        "plot_data": {
            "image": encoded_image,
            "content_type": "image/png",
            "encoding": "base64"
        }
    }
    return response
