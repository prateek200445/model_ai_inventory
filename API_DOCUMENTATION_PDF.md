# Inventory Forecasting & Tariff Impact APIs
## Technical Documentation v1.0

---

# Table of Contents
1. [Quick Start](#quick-start)
2. [Inventory Forecasting API](#inventory-forecasting-api)
3. [Tariff Impact API](#tariff-impact-api)
4. [Error Handling](#error-handling)
5. [Security & Rate Limits](#security--rate-limits)
6. [Code Examples](#code-examples)

---

# Quick Start

## Base URLs
```
Inventory API: https://inventory-forecast-api.onrender.com
Tariff API:    https://tariff-impact-api.onrender.com
```

## Authentication
No authentication required. APIs are open but rate-limited.

---

# Inventory Forecasting API

## Core Features
- Demand forecasting up to 30 days
- Inventory level recommendations
- Safety stock calculations
- Reorder point optimization
- Visual trend analysis

## Main Endpoint: `/forecast`

### Request Format
```json
POST /forecast
{
    "days": 7,                    // Required: 1-30 days
    "product_id": "PROD123",      // Optional: Filter by product
    "category": "Electronics",    // Optional: Product category
    "region": "North",           // Optional: Regional filter
    "min_rating": 4.0,           // Optional: Minimum rating
    "max_price": 1000,           // Optional: Price ceiling
    "min_discount": 10           // Optional: Minimum discount %
}
```

### Response Format
```json
{
    "Reorder Point": 100,
    "Safety Stock": 50,
    "Minimum Level": 50,
    "Maximum Level": 200,
    "Forecast": {
        "2025-10-04": {
            "forecast": 120,
            "lower_bound": 100,
            "upper_bound": 140
        }
        // ... more dates
    },
    "Plot File": "forecast_plot.png",
    "Warnings": [
        "🚨 Important Notice for Product PROD123:",
        "• Current stock: 150 units",
        "• Duration: 15 days",
        "• Daily average: 10 units"
    ]
}
```

### Practical Example
```javascript
const getInventoryForecast = async (productId) => {
    try {
        const response = await fetch(
            'https://inventory-forecast-api.onrender.com/forecast',
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    days: 7,
                    product_id: productId
                })
            }
        );
        return await response.json();
    } catch (error) {
        console.error('Forecast error:', error);
        throw error;
    }
};
```

---

# Tariff Impact API

## Core Features
- Tariff change impact analysis
- Environmental impact assessment
- Economic implications
- Trade flow predictions
- Sustainability recommendations

## Main Endpoint: `/analyze_impact`

### Request Format
```json
POST /analyze_impact
{
    "current_tariff": 10.5,      // Required: Current rate %
    "proposed_tariff": 15.0,     // Required: New rate %
    "product_category": "Electronics",  // Required
    "trade_volume": 1000000,     // Required: Annual USD
    "country_of_origin": "China" // Required
}
```

### Response Format
```json
{
    "analysis": {
        "economic_impact": {
            "cost_increase": 45000,
            "price_impact": 4.5,
            "trade_flow_impact": "Moderate decrease expected"
        },
        "environmental_impact": {
            "carbon_footprint": "3% reduction potential",
            "sustainability_score": 7.5,
            "recommendations": [
                "Consider local sourcing",
                "Optimize logistics"
            ]
        },
        "recommendations": [
            "Phase tariff changes",
            "Monitor market response",
            "Explore alternatives"
        ]
    }
}
```

### Practical Example
```javascript
const analyzeTariffImpact = async (params) => {
    try {
        const response = await fetch(
            'https://tariff-impact-api.onrender.com/analyze_impact',
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    current_tariff: params.current,
                    proposed_tariff: params.proposed,
                    product_category: params.category,
                    trade_volume: params.volume,
                    country_of_origin: params.country
                })
            }
        );
        return await response.json();
    } catch (error) {
        console.error('Analysis error:', error);
        throw error;
    }
};
```

---

# Error Handling

## Status Codes
- 200: Success
- 400: Bad Request
- 422: Validation Error
- 500: Server Error

## Error Response Format
```json
{
    "detail": {
        "msg": "Error description",
        "type": "error_type"
    }
}
```

## Error Handling Example
```javascript
try {
    const response = await fetch(apiUrl, options);
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail.msg);
    }
    return await response.json();
} catch (error) {
    console.error('API Error:', error);
    // Handle error appropriately
}
```

---

# Security & Rate Limits

## CORS Configuration
Allowed Origins:
- https://sustain-a-thon-8yn8.vercel.app
- http://localhost:3000 (development)

## Rate Limits
- 100 requests per minute per IP
- 1000 requests per hour per IP

## Best Practices
1. Implement caching
2. Use batch requests when possible
3. Handle rate limit errors gracefully
4. Implement retry logic with exponential backoff

---

# Code Examples

## React Integration Example
```jsx
import { useState, useEffect } from 'react';

const InventoryDashboard = ({ productId }) => {
    const [forecast, setForecast] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchForecast = async () => {
            setLoading(true);
            try {
                const response = await fetch(
                    'https://inventory-forecast-api.onrender.com/forecast',
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            days: 7,
                            product_id: productId 
                        })
                    }
                );
                const data = await response.json();
                setForecast(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        if (productId) {
            fetchForecast();
        }
    }, [productId]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!forecast) return <div>No data available</div>;

    return (
        <div>
            <h2>Inventory Forecast</h2>
            <div>
                <h3>Reorder Point: {forecast.ReorderPoint}</h3>
                <h3>Safety Stock: {forecast.SafetyStock}</h3>
                {/* Add more visualization components */}
            </div>
        </div>
    );
};

export default InventoryDashboard;
```

## Vue.js Integration Example
```javascript
<template>
  <div class="tariff-analysis">
    <h2>Tariff Impact Analysis</h2>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else-if="analysis">
      <div class="economic-impact">
        <h3>Economic Impact</h3>
        <p>Cost Increase: ${{ analysis.economic_impact.cost_increase }}</p>
        <p>Price Impact: {{ analysis.economic_impact.price_impact }}%</p>
      </div>
      <div class="recommendations">
        <h3>Recommendations</h3>
        <ul>
          <li v-for="rec in analysis.recommendations" :key="rec">
            {{ rec }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TariffAnalysis',
  data() {
    return {
      analysis: null,
      loading: false,
      error: null
    }
  },
  methods: {
    async analyzeTariff(params) {
      this.loading = true;
      try {
        const response = await fetch(
          'https://tariff-impact-api.onrender.com/analyze_impact',
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
          }
        );
        this.analysis = await response.json();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
```

---

# Support & Resources

## Getting Help
- GitHub Issues: https://github.com/prateek200445/model_ai_inventory/issues
- Email Support: [your-support-email]

## Version Information
- API Version: 1.0.0
- Last Updated: October 2025
- Status: Production

---

*This documentation is maintained by the AI Inventory & Tariff Analysis Team*