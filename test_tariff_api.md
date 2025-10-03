# How to Use the Tariff Impact Analysis API

'''
The API provides tariff impact analysis in two modes:

1. Product-specific analysis:
   - Requires product_id and tariff_percentage
   - Category is optional
   
2. Category-level analysis:
   - Requires category and tariff_percentage
   - product_id should be null or omitted

Example curl commands:

1. Product-specific analysis:
```bash
curl -X POST "http://localhost:8001/analyze_tariff" \
     -H "Content-Type: application/json" \
     -d '{
           "product_id": "PROD001",
           "tariff_percentage": 15,
           "category": "Electronics"
         }'
```

2. Category-level analysis:
```bash
curl -X POST "http://localhost:8001/analyze_tariff" \
     -H "Content-Type: application/json" \
     -d '{
           "tariff_percentage": 10,
           "category": "Electronics"
         }'
```

Python example using requests:
'''

import requests
import json

def test_tariff_analysis():
    # API endpoint
    url = "http://localhost:8001/analyze_tariff"
    
    # Example 1: Product-specific analysis
    product_data = {
        "product_id": "PROD001",  # Replace with actual product ID
        "tariff_percentage": 15,
        "category": "Electronics"  # Replace with actual category
    }
    
    print("\nTesting Product-specific Analysis:")
    print("Request:", json.dumps(product_data, indent=2))
    response = requests.post(url, json=product_data)
    print("Response:", json.dumps(response.json(), indent=2))
    
    # Example 2: Category-level analysis
    category_data = {
        "tariff_percentage": 10,
        "category": "Electronics"  # Replace with actual category
    }
    
    print("\nTesting Category-level Analysis:")
    print("Request:", json.dumps(category_data, indent=2))
    response = requests.post(url, json=category_data)
    print("Response:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_tariff_analysis()