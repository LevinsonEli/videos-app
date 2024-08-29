FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py app.py
COPY templates templates
COPY static static
COPY ./src ./src

EXPOSE 5000

VOLUME /app/.env

ENTRYPOINT ["python3", "app.py"]
