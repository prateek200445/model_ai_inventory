from model import forecast

if __name__ == "__main__":
    results = forecast(7)   # run forecast for 7 days
    print("=== Forecast Results ===")
    for k, v in results.items():
        print(f"{k}: {v}")
