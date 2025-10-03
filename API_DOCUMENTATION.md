# API Documentation

## Base URLs
- Inventory Forecasting API: `https://inventory-forecast-api.onrender.com`
- Tariff Impact API: `https://tariff-impact-api.onrender.com`

Base URL: `https://model-ai-inventory.onrender.com`

## Endpoints

### 1. Health Check
- **URL**: `/`
- **Method**: GET
- **Description**: Check if the API is running
- **Response**: Text message confirming API status

Example:
```python
import requests

response = requests.get('https://model-ai-inventory.onrender.com/')
print(response.text)  # Should return "Hello from the Inventory Forecasting API!"
```

### 2. Forecast Data
- **URL**: `/forecast`
- **Method**: GET
- **Parameters**:
  - `days` (optional, integer): Number of days to forecast [default: 7]
  - `product_id` (optional, string): Filter by product ID (e.g., "P017")
  - `category` (optional, string): Filter by category (e.g., "A", "B", "C")
  - `region` (optional, string): Filter by region (e.g., "North", "South", "East", "West")
  - `min_rating` (optional, float): Filter by minimum rating (1-5)
  - `max_price` (optional, float): Filter by maximum price
  - `min_discount` (optional, float): Filter by minimum discount percentage

Example Request:
```python
import requests

# Example 1: Basic forecast
response = requests.get('https://model-ai-inventory.onrender.com/forecast')
data = response.json()

# Example 2: Forecast with filters
params = {
    'days': 7,
    'product_id': 'P017',
    'category': 'A',
    'region': 'North',
    'min_rating': 4.0,
    'max_price': 100,
    'min_discount': 5
}
response = requests.get('https://model-ai-inventory.onrender.com/forecast', params=params)
data = response.json()
```

Response Format:
```json
{
    "Reorder Point": 250,
    "Safety Stock": 100,
    "Minimum Level": 100,
    "Maximum Level": 450,
    "Forecast": {
        "2025-09-14": 235.45,
        "2025-09-15": 242.12,
        // ... more dates
    },
    "Warnings": [
        "✅ Inventory levels are within optimal range (100 - 450 units)"
    ]
}
```

### 3. Visualization Plot
- **URL**: `/plot`
- **Method**: GET
- **Description**: Get a visualization of the forecast
- **Response**: Base64 encoded PNG image

Example:
```python
import requests

# Get plot as base64 string
response = requests.get('https://model-ai-inventory.onrender.com/plot')
plot_data = response.text

# Save as image file
import base64
with open('forecast_plot.png', 'wb') as f:
    f.write(base64.b64decode(plot_data))
```

## Usage in Different Languages

### JavaScript/Node.js
```javascript
// Using fetch
fetch('https://model-ai-inventory.onrender.com/forecast?days=7&product_id=P017')
  .then(response => response.json())
  .then(data => console.log(data));

// Using axios
const axios = require('axios');
axios.get('https://model-ai-inventory.onrender.com/forecast', {
  params: {
    days: 7,
    product_id: 'P017'
  }
})
.then(response => console.log(response.data));
```

### Java
```java
import java.net.URI;
import java.net.http.*;

HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://model-ai-inventory.onrender.com/forecast?days=7"))
    .build();
HttpResponse<String> response = client.send(request, 
    HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());
```

### cURL (Command Line)
```bash
# Get forecast
curl "https://model-ai-inventory.onrender.com/forecast?days=7&product_id=P017"

# Get plot
curl "https://model-ai-inventory.onrender.com/plot" > forecast_plot.png
```

## Error Handling

The API may return the following HTTP status codes:
- 200: Successful request
- 400: Bad request (invalid parameters)
- 404: Not found
- 500: Server error

Error Response Format:
```json
{
    "error": "Error message description",
    "detail": "Additional error details if available"
}
```

## Rate Limits and Usage
- The API is hosted on Render.com
- Please implement reasonable request rates
- Large numbers of requests in short periods may be throttled

## Data Update Frequency
- The forecast model uses historical data from the dataset
- Data is updated daily
- Forecasts are generated in real-time for each request

## Support
For issues or questions, please create an issue in the GitHub repository:
https://github.com/prateek200445/model_ai_inventory