import requests
import json

def test_tariff_analysis():
    url = "http://localhost:8001/analyze_tariff"
    headers = {"Content-Type": "application/json"}
    data = {
        "tariff_percentage": 10,
        "category": "Electronics"
    }
    
    try:
        response = requests.post(url, json=data)
        print("Status Code:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_tariff_analysis()