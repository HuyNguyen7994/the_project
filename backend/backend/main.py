from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import pika
from typing import Literal

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


class Message(BaseModel):
    content: str


class EtlPayload(BaseModel):
    etl_name: Literal["gsheet"]
    payload: dict


@app.get("/api/v1/health")
def check_health():
    return {"status": "healthy"}


@app.post("/api/v1/etl/run", status_code=204)
def run_etl(etl_payload: EtlPayload):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port="5672",
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="run_etl")
    channel.basic_publish(exchange="", routing_key="run_etl", body=etl_payload)
