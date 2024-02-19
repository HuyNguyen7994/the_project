from etl.source.aqicn import extract_current_timestamp, write_to_postgres_pm25, extract_current_pm25
import datetime
from pytz import timezone
import logging
import psycopg as pg

logger = logging.getLogger(__name__)

SAMPLE_DATA = {
    "status": "ok",
    "data": {
        "time": {"iso": "2024-02-16T13:00:00+07:00"},
        "idx": 13659,
        "city": {
            "geo": [11.030287, 106.35631],
            "name": "Tây Ninh/Thị xã Tràng Bảng, Vietnam",
            "url": "https://aqicn.org/city/vietnam/tay-ninh/thi-xa-trang-bang",
            "location": "",
        },
        "iaqi": {
            "dew": {"v": 21},
            "h": {"v": 58},
            "no2": {"v": 23},
            "p": {"v": 1014},
            "pm10": {"v": 62},
            "pm25": {"v": 41},
        },
    },
}
SAMPLE_TS_NOT_TZ = {
    "status": "ok",
    "data": {
        "time": {"iso": "2024-02-19T06:00:00Z"},
    }
}
SAMPLE_DATA_MISSING_CUR_PM25 = {
    "data": {
        "iaqi": {
            "pm10": {"v": 62},
        },
    },
}
CONNINFO = "host=localhost port=5432 dbname=test user=postgres password=postgres"
CREATE_TABLES = """
create table historical_pm25 (
    etl_ts timestamp with time zone,
    station_id bigint,
    city_name text,
    station_ts timestamp with time zone,
    pm25_value smallint
);
"""
DROP_TABLES = """
drop table historical_pm25;
"""


def test_extract_current_timestamp():
    timestamp = extract_current_timestamp(SAMPLE_DATA)
    logger.error(timestamp)
    expected_timestamp = datetime.datetime(
        2024, 2, 16, 13, 0, 0, tzinfo=timezone("Etc/GMT+7")
    )
    assert (
        timestamp.utcoffset().total_seconds()
        + expected_timestamp.utcoffset().total_seconds()
    ) == 0  # quirky timezone
    assert timestamp.replace(tzinfo=None) == expected_timestamp.replace(tzinfo=None)
    wrong_timestamp = datetime.datetime(
        2024, 2, 16, 13, 0, 0, tzinfo=timezone("Etc/GMT+8")
    )
    assert (
        not (
            timestamp.utcoffset().total_seconds()
            + wrong_timestamp.utcoffset().total_seconds()
        )
        == 0
    )

def test_extract_current_timestamp_notimezone():
    ts = extract_current_timestamp(SAMPLE_TS_NOT_TZ)

def test_missing_current_pm():
    assert not extract_current_pm25(SAMPLE_DATA_MISSING_CUR_PM25)

def test_postgres_single():
    try:
        with pg.connect(conninfo=CONNINFO) as connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TABLES)
        write_to_postgres_pm25(
            conninfo=CONNINFO, json_data=SAMPLE_DATA, etl_ts=datetime.datetime.now()
        )
        with pg.connect(conninfo=CONNINFO) as connection:
            with connection.cursor() as cursor:
                cursor.execute("select count(*) from historical_pm25")
                assert cursor.fetchone() == (1,)
    finally:
        with pg.connect(conninfo=CONNINFO) as connection:
            with connection.cursor() as cursor:
                cursor.execute(DROP_TABLES)

def test_postgres_dedup():
    try:
        with pg.connect(conninfo=CONNINFO) as connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_TABLES)
        write_to_postgres_pm25(
            conninfo=CONNINFO, json_data=SAMPLE_DATA, etl_ts=datetime.datetime.now()
        )
        write_to_postgres_pm25(
            conninfo=CONNINFO, json_data=SAMPLE_DATA, etl_ts=datetime.datetime.now()
        )
        with pg.connect(conninfo=CONNINFO) as connection:
            with connection.cursor() as cursor:
                cursor.execute("select count(*) from historical_pm25")
                assert cursor.fetchone() == (1,)
    finally:
        with pg.connect(conninfo=CONNINFO) as connection:
            with connection.cursor() as cursor:
                cursor.execute(DROP_TABLES)
                pass