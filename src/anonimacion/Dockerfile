FROM python:3.10

WORKDIR /app
EXPOSE 5001/tcp

COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY src/anonimacion /app/src/anonimacion

ENV FLASK_APP=src.anonimacion.api
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONPATH="/app/src"

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

