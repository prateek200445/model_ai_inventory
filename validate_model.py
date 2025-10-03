# validate_model.py
from model import forecast
import pandas as pd
import numpy as np

def validate_forecast_values(forecast_data):
    print("\n=== Validating Forecast Values ===")
    all_valid = True
    
    for date, values in forecast_data['Forecast'].items():
        forecast_value = values['forecast']
        lower_bound = values['lower_bound']
        upper_bound = values['upper_bound']
        
        # Check 1: Positive numbers
        if forecast_value < 0:
            print(f"❌ Negative forecast value for {date}: {forecast_value}")
            all_valid = False
        
        # Check 2 & 3: Bounds relationship
        if not (lower_bound <= forecast_value <= upper_bound):
            print(f"❌ Invalid bounds for {date}:")
            print(f"   Lower: {lower_bound} <= Forecast: {forecast_value} <= Upper: {upper_bound}")
            all_valid = False
    
    if all_valid:
        print("✅ All forecast values and bounds are valid")
    return all_valid

def validate_inventory_levels(forecast_data):
    print("\n=== Validating Inventory Levels ===")
    all_valid = True
    
    # Get inventory parameters
    reorder_point = forecast_data['Reorder Point']
    safety_stock = forecast_data['Safety Stock']
    min_level = forecast_data['Minimum Level']
    max_level = forecast_data['Maximum Level']
    
    # Check relationships
    if not (0 <= safety_stock <= reorder_point <= max_level):
        print("❌ Invalid inventory level relationship:")
        print(f"   Safety Stock: {safety_stock}")
        print(f"   Reorder Point: {reorder_point}")
        print(f"   Maximum Level: {max_level}")
        all_valid = False
    
    if not (min_level <= max_level):
        print("❌ Minimum level greater than maximum level:")
        print(f"   Min Level: {min_level}")
        print(f"   Max Level: {max_level}")
        all_valid = False
    
    # Check reasonable ranges (based on forecast values)
    forecast_values = [v['forecast'] for v in forecast_data['Forecast'].values()]
    avg_forecast = np.mean(forecast_values)
    
    if max_level < avg_forecast or min_level > avg_forecast:
        print("❌ Inventory levels don't align with forecast values:")
        print(f"   Average Forecast: {avg_forecast:.2f}")
        print(f"   Min Level: {min_level}")
        print(f"   Max Level: {max_level}")
        all_valid = False
    
    if all_valid:
        print("✅ All inventory levels are reasonable")
    return all_valid

def validate_warnings(forecast_data):
    print("\n=== Validating Warnings ===")
    all_valid = True
    
    warnings = forecast_data['Warnings']
    forecast_values = [v['forecast'] for v in forecast_data['Forecast'].values()]
    max_forecast = max(forecast_values)
    min_forecast = min(forecast_values)
    
    # Check if warnings match the data
    has_high_stock_warning = any("High stock alert" in w for w in warnings)
    has_low_stock_warning = any("Low stock risk" in w for w in warnings)
    
    if max_forecast > forecast_data['Maximum Level'] and not has_high_stock_warning:
        print("❌ Missing high stock warning when forecast exceeds maximum level")
        all_valid = False
    
    if min_forecast < forecast_data['Minimum Level'] and not has_low_stock_warning:
        print("❌ Missing low stock warning when forecast below minimum level")
        all_valid = False
    
    if all_valid:
        print("✅ Warnings are consistent with forecast data")
    return all_valid

def run_validation_tests():
    print("🔍 Starting Model Validation\n")
    
    # Test cases
    test_cases = [
        {"name": "Basic Forecast", "params": {"days": 7}},
        {"name": "Filtered Forecast", "params": {
            "days": 7,
            "product_id": "P017",
            "category": "A"
        }},
        {"name": "Price-Filtered Forecast", "params": {
            "days": 7,
            "max_price": 50
        }}
    ]
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        print("-" * 50)
        
        try:
            # Get forecast results
            results = forecast(**test_case['params'])
            
            # Run validations
            validations = [
                validate_forecast_values(results),
                validate_inventory_levels(results),
                validate_warnings(results)
            ]
            
            # Overall test case result
            if all(validations):
                print(f"\n✅ {test_case['name']}: All validations passed")
            else:
                print(f"\n❌ {test_case['name']}: Some validations failed")
                
        except Exception as e:
            print(f"\n❌ Error during validation: {str(e)}")

if __name__ == "__main__":
    run_validation_tests()