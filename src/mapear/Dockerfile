FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY src/mapear /app/src/mapear

ENV FLASK_APP=src.mapear.api
ENV FLASK_ENV=development
ENV PYTHONPATH="/app/src"

RUN pip install requests==2.28.2

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

