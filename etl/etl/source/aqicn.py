import requests as rq
from typing import TypedDict
from datetime import datetime
import psycopg
import pandas as pd
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


def get_gelocalized_feed(lat: str, lng: str, token: str) -> AQResponse:
    url = f"https://api.waqi.info/feed/geo:{lat};{lng}/?token={token}"
    return rq.get(url).json()


def extract_current_pm25(json_data: AQResponse) -> int:
    return json_data["data"]["iaqi"]["pm25"]["v"]


def extract_forecast_pm25(json_data: AQResponse) -> list[AQForecastIndex]:
    return json_data["data"]["forecast"]["pm25"]


def extract_current_timestamp(json_data: AQResponse) -> datetime:
    return datetime.fromisoformat(json_data["data"]["time"]["iso"])


def extract_monitoring_station(json_data: AQResponse) -> int:
    return json_data["data"]["idx"]


def write_to_postgres_pm25(conninfo: str, json_data: AQResponse):
    with psycopg.connect(conninfo=conninfo) as connection:
        with connection.cursor() as cursor:
            current_timestamp = extract_current_timestamp(json_data)
            monitoring_station = extract_monitoring_station(json_data)
            cursor.execute(
                f"select count(*) from historical_pm25 where timestamp = {current_timestamp} and station_id = {monitoring_station}"
            )
            if cursor.fetchone()[0] > 0:
                logger.warning("No new data from API. Skipped update.")
                return
            current_pm25 = extract_forecast_pm25(json_data)
            cursor.execute(
                f"insert into historical_pm25 (timestamp,station_id,pm25_value) values ({current_timestamp, monitoring_station, current_pm25})"
            )
            cursor.execute(
                "insert into forecast_pm25 (forecast_timestamp,stationd_id,forecast_date,avg_pm25,min_pm25,max_pm25) values()"
            )


def main():
    pass
