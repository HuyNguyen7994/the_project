import requests as rq
from typing import TypedDict
from datetime import datetime
import psycopg
from loguru import logger


class AQCity(TypedDict):
    name: str
    geo: list[float]
    url: str


class AQTime(TypedDict):
    s: str
    tz: str
    v: int
    iso: str


class AQCurrentValue(TypedDict):
    v: int


class AQCurrentIndex(TypedDict):
    pm10: AQCurrentValue
    pm25: AQCurrentValue


class AQForecastValue(TypedDict):
    avg: int
    day: str
    max: int
    min: int


class AQForecastIndex(TypedDict):
    pm10: list[AQCurrentValue]
    pm25: list[AQCurrentValue]


class AQData(TypedDict):
    idx: int
    aqi: int
    time: AQTime
    city: AQCity
    attributions: list[dict]
    iaqi: AQCurrentIndex
    forecast: AQForecastIndex


class AQResponse(TypedDict):
    status: str
    data: AQData


def get_gelocalized_feed(lat: str, lng: str, token: str) -> tuple[AQResponse, datetime]:
    etl_ts = datetime.now()
    url = f"https://api.waqi.info/feed/geo:{lat};{lng}/?token={token}"
    return rq.get(url).json(), etl_ts


def extract_current_pm25(json_data: AQResponse) -> int:
    return json_data["data"]["iaqi"]["pm25"]["v"]


def extract_forecast_pm25(json_data: AQResponse) -> list[AQForecastIndex]:
    return json_data["data"]["forecast"]["pm25"]


def extract_current_timestamp(json_data: AQResponse) -> datetime:
    return datetime.fromisoformat(json_data["data"]["time"]["iso"])


def extract_monitoring_station(json_data: AQResponse) -> int:
    return json_data["data"]["idx"]

def insert_historical_pm25(cursor: psycopg.Cursor, etl_ts: datetime, station_id: int, station_ts: datetime, pm25_value: int):
    cursor.execute("insert into historical_pm25 (etl_ts, station_id, station_ts, pm25_value) values (%s, %s, %s, %s)",[etl_ts, station_id, station_ts, pm25_value])


def write_to_postgres_pm25(conninfo: str, json_data: AQResponse, etl_ts: datetime):
    with psycopg.connect(conninfo=conninfo) as connection:
        with connection.cursor() as cursor:
            station_id = extract_monitoring_station(json_data)
            station_ts = extract_current_timestamp(json_data)
            check_query = f"select count(*) from historical_pm25 where station_id = {station_id} and station_ts >= '{station_ts}'"
            logger.debug(check_query)
            cursor.execute(check_query)
            if cursor.fetchone()[0] > 0:
                logger.warning("No new data from API. Skipped update.")
                return
            pm25_value = extract_current_pm25(json_data)
            insert_historical_pm25(cursor, etl_ts, station_id, station_ts, pm25_value)


def main():
    pass