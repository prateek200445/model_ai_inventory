import requests
import json

# API endpoint
BASE_URL = "http://127.0.0.1:8000"

def test_forecast_api():
    # Test 1: Basic forecast
    print("\nTest 1: Basic 7-day forecast")
    data = {
        "days": 7,
        "product_id": None,
        "category": "Electronics"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/forecast",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

    # Test 2: Product-specific forecast
    print("\nTest 2: Product-specific forecast")
    data = {
        "days": 14,
        "product_id": "PROD001",
        "category": "Electronics",
        "min_rating": 4.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/forecast",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_forecast_api()