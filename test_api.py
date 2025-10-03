import requests
import json

# Base URL of your FastAPI application
BASE_URL = "http://localhost:8000"

# Test Case 1: Analysis for a specific product
product_request = {
    "product_id": "P123",  # Replace with an actual product ID from your dataset
    "tariff_percentage": 15,  # Example: 15% tariff
    "category": "Electronics"  # Optional: can be omitted
}

# Make the request
response = requests.post(f"{BASE_URL}/analyze_tariff", json=product_request)
print("\nProduct-specific analysis:")
print(json.dumps(response.json(), indent=2))

# Test Case 2: Category-level analysis
category_request = {
    "product_id": None,
    "tariff_percentage": 10,
    "category": "Electronics"
}

# Make the request
response = requests.post(f"{BASE_URL}/analyze_tariff", json=category_request)
print("\nCategory-level analysis:")
print(json.dumps(response.json(), indent=2))