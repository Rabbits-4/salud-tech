from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import json

MAPEAR_URL = os.getenv("MAPEAR_URL")

app = FastAPI()

class AmorResponse(BaseModel):
    message: str

@app.get("/obtener-parquets", response_model=AmorResponse)
async def obtener_parquets():
    print(f"http://{MAPEAR_URL}/mapear/obtener-parquets")
    response = requests.get(f"http://{MAPEAR_URL}/mapear/obtener-parquets")
    print("***** after request")
    print(f"response: {response}")
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)