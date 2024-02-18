import os
import json
import pika
import logging
import psycopg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can adjust the HTTP methods as needed
    allow_headers=["*"],  # You can adjust the HTTP headers as needed
)


@app.get("/api/v1/health")
def check_health():
    return {"status": "healthy"}


@app.post("/api/v1/etl/run/{etl_pipeline}/{latitude}/{longtitude}", status_code=204)
def run_etl(etl_pipeline: str, latitude: str, longtitude: str):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=os.getenv("RABBITMQ_PORT"),
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="run_etl")
    channel.basic_publish(
        exchange="",
        routing_key="run_etl",
        body=json.dumps(
            {"command": etl_pipeline, "payload": {"lat": latitude, "lng": longtitude}}
        ),
    )


@app.get("/api/v1/aqicn/recent/{num}")
def get_recent_air_quality(num: int):
    with psycopg.connect(conninfo=os.getenv("POSTGRES_CONNINFO")) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from historical_pm25 order by etl_ts limit %s", (num,))
            return cursor.fetchall()