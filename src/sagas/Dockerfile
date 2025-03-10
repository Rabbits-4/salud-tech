# Usa una imagen de Python ligera
FROM python:3.10-slim

# Define el directorio de trabajo
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY src/sagas /app/src/sagas

COPY requirements.txt .

# Copia los archivos de la aplicación
ENV PYTHONPATH=/app/src

RUN pip install -r src/sagas/requirements.txt

# Comando para ejecutar el coordinador de sagas
CMD ["python", "src/sagas/main.py"]
