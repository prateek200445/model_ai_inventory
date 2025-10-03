import requests
import json
import pandas as pd
import os

def load_sample_data():
    """Load sample data from the CSV file"""
    try:
        df = pd.read_csv('large_dataset.csv')
        sample_product = df.iloc[0]
        return {
            'product_id': str(sample_product['product_id']),
            'category': str(sample_product['category'])
        }
    except Exception as e:
        print(f"Warning: Could not load sample data: {e}")
        return {
            'product_id': 'PROD001',
            'category': 'Electronics'
        }

def test_api():
    """Test the tariff analysis API"""
    # You can configure this URL via environment variable for different environments
    url = os.getenv('API_URL', 'http://127.0.0.1:8001/analyze_tariff')
    sample_data = load_sample_data()
    
    # Test cases
    test_requests = [
        {
            "name": "Category Analysis",
            "data": {
                "tariff_percentage": 10.0,
                "category": sample_data['category']
            }
        },
        {
            "name": "Product Analysis",
            "data": {
                "product_id": sample_data['product_id'],
                "tariff_percentage": 15.0,
                "category": sample_data['category']
            }
        }
    ]
    
    # Run tests
    for test in test_requests:
        print(f"\nTesting {test['name']}:")
        print(f"Request data: {json.dumps(test['data'], indent=2)}")
        
        try:
            response = requests.post(
                url,
                json=test['data'],
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the server. Make sure it's running on http://127.0.0.1:8001")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_api()