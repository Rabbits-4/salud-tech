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
    raw_response = requests.get(f"http://{MAPEAR_URL}/mapear/obtener-parquets")
    response = raw_response.json()

    return {
        "data": [{"token":item["historial_paciente_id"], "fecha_creacion": item["fecha_creacion"], "contexto_procesal": item["contexto_procesal"]} for item in response]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)