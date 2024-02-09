from typing import Union

from fastapi import FastAPI
from app.workers.echo import echo_func
from app.workers.database import SqliteConnection
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
from pathlib import Path
import logging

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

def _get_database_conn_str():
    path = str(Path(__file__).parent.parent / "database" / "prod.db")
    logger.info(path)
    return path

@app.get("api/v1/health")
def check_health():
    return {"status": "healthy"}


@app.post("api/v1/checkin/{participant}")
def increment_checkin(participant: str):
    today = datetime.date.today()
    with SqliteConnection(_get_database_conn_str()) as connection:
        cursor = connection.cursor()
        cursor.execute("insert into checkin (participant, checkin_date) values (?, ?)", [participant, today])
    return {"participant": participant, "checkin": today}

@app.post("api/v1/message/{participant}")
def echo(participant, message: Message):
    return {"sender": participant, "content" : message.content}