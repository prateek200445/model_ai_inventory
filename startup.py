import uvicorn

if __name__ == "__main__":
    uvicorn.run("tariff_api:app", host="0.0.0.0", port=8000)