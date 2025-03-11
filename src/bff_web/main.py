from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
import json
from typing import List

MAPEAR_URL = os.getenv("MAPEAR_URL")

app = FastAPI()

class RespuestaWeb(BaseModel):
    data: List[dict]

@app.get("/obtener-parquets", response_model=RespuestaWeb)
async def obtener_parquets():
    print(f"http://{MAPEAR_URL}/mapear/obtener-parquets")
    response = requests.get(f"http://{MAPEAR_URL}/mapear/obtener-parquets")
    print("***** after request")
    print(f"response: {response.json()}")
    return {
        "data": response.json()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)