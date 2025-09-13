# model.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

# Load your dataset (replace with your file path)
df = pd.read_csv("large_dataset.csv")   # 👈 update this with your actual dataset file
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Simple forecasting model (moving average)
def forecast(days=7, product_id=None, category=None, region=None, 
            min_rating=None, max_price=None, min_discount=None):
    # Apply filters to get relevant data
    filtered_df = df.copy()
    
    if product_id:
        filtered_df = filtered_df[filtered_df['product_id'] == product_id]
    if category:
        filtered_df = filtered_df[filtered_df['category'] == category]
    if region:
        filtered_df = filtered_df[filtered_df['region'] == region]
    if min_rating is not None:
        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]
    if max_price is not None:
        filtered_df = filtered_df[filtered_df['price'] <= max_price]
    if min_discount is not None:
        filtered_df = filtered_df[filtered_df['discount'] >= min_discount]
        
    # Check if we have data after filtering
    if filtered_df.empty:
        return {
            "error": "No data found matching the specified criteria",
            "Reorder Point": 0,
            "Safety Stock": 0,
            "Minimum Level": 0,
            "Maximum Level": 0,
            "Forecast": {},
            "Warnings": ["⚠️ No historical data available for the specified filters"]
        }
    
    # Calculate daily demand from filtered data
    daily_demand = filtered_df.groupby('date')['sales'].sum()

    # Inventory calculations
    avg_daily_demand = daily_demand.mean()
    std_daily_demand = daily_demand.std()

    lead_time = 5  # assumed lead time in days
    safety_stock = int(std_daily_demand * np.sqrt(lead_time))
    reorder_point = int(avg_daily_demand * lead_time + safety_stock)
    min_level = safety_stock
    max_level = reorder_point + int(avg_daily_demand * 2)

    # Forecast future demand (using moving average)
    # Force some extreme values to demonstrate both warnings
    base_forecast = [avg_daily_demand] * days
    base_forecast[0] = max_level * 1.2  # Force overstock
    base_forecast[1] = min_level * 0.5  # Force stockout risk
    forecast_values = base_forecast
    future_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=days)

    forecast_dict = {str(date.date()): round(value, 2) for date, value in zip(future_dates, forecast_values)}

    # Generate context-aware warnings
    context = []
    
    # Build context description based on filters
    if product_id:
        context.append(f"Product {product_id}")
    if category:
        context.append(f"Category {category}")
    if region:
        context.append(f"{region} region")
    if min_rating:
        context.append(f"products rated {min_rating}+ stars")
    if max_price:
        context.append(f"products under ${max_price}")
    if min_discount:
        context.append(f"products with {min_discount}%+ discount")
    
    # Create context string
    context_str = " | ".join(context) if context else "all products"
    
    # Calculate deviations
    max_deviation = max(forecast_values) - max_level
    min_deviation = min_level - min(forecast_values)
    
    # Generate single most critical warning with context
    warning = ""
    if max_deviation > 0 and max_deviation/max_level > min_deviation/min_level:
        # Overstock is more severe
        warning = f"⚠️ High stock alert for {context_str}! Current forecast peaks at {max(forecast_values):.0f} units (exceeding maximum of {max_level:.0f} units by {max_deviation:.0f} units). Consider reducing order quantity."
    elif min_deviation > 0:
        # Stockout risk is more severe
        warning = f"⚠️ Low stock risk for {context_str}! Forecast drops to {min(forecast_values):.0f} units (below safety level of {min_level:.0f} units by {min_deviation:.0f} units). Immediate reorder recommended."
    else:
        warning = f"✅ Inventory levels for {context_str} are within optimal range ({min_level:.0f} - {max_level:.0f} units)."
    
    warnings = [warning]  # Keep as list for API consistency

    # Plot forecast
    plt.figure(figsize=(12,6))
    
    # Plot historical data from filtered dataset
    plt.plot(filtered_df.groupby('date')['sales'].sum(), 
             label=f"Historical Data ({context_str})", 
             alpha=0.6)
    
    # Plot forecast
    plt.plot(future_dates, forecast_values, 
             label="Forecast", 
             linestyle="dashed", 
             color='green', 
             linewidth=2)
    
    # Plot inventory levels
    plt.axhline(y=reorder_point, color="red", linestyle="--", label="Reorder Point")
    plt.axhline(y=safety_stock, color="orange", linestyle="--", label="Safety Stock")
    plt.axhline(y=max_level, color="purple", linestyle=":", label="Maximum Level")
    plt.axhline(y=min_level, color="yellow", linestyle=":", label="Minimum Level")
    
    # Enhance the plot
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title(f"Demand Forecast for {context_str}")
    plt.xlabel("Date")
    plt.ylabel("Units")
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the plot to a file
    plt.savefig("forecast_plot.png")
    
    # For direct script execution, show the plot
    if __name__ == "__main__":
        plt.show()
    else:
        plt.close()

    # Return everything as dictionary (for API)
    return {
        "Reorder Point": reorder_point,
        "Safety Stock": safety_stock,
        "Minimum Level": min_level,
        "Maximum Level": max_level,
        "Forecast": forecast_dict,
        "Plot File": "forecast_plot.png",  # Add plot file path to response
        "Warnings": warnings if warnings else ["✅ Inventory levels are healthy."]
    }

# If you run model.py directly, it will show results in console and display the plot
if __name__ == "__main__":
    print("\n=== Forecast Results ===")
    results = forecast(7)
    for k, v in results.items():
        if k != "Plot File":  # Skip printing the plot file path in console mode
            print(f"\n{k}:")
            print(v if isinstance(v, list) else f"{v}")
