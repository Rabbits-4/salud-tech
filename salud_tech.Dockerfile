FROM python:3.10

WORKDIR /app
EXPOSE 5000/tcp

COPY requirements.txt /app/
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV FLASK_ENV=development

CMD [ "flask", "--app", "src/salud_tech/api", "run", "--host=0.0.0.0", "--reload"]
