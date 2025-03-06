FROM python:3.10

WORKDIR /app
EXPOSE 5000/tcp

COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY src/salud_tech /app/src/salud_tech

ENV FLASK_APP=src.salud_tech.api
ENV PYTHONPATH="/app/src"

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

