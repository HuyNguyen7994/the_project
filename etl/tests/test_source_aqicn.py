from etl.source.aqicn import extract_current_timestamp
import datetime
from pytz import timezone
import logging
import pytest
import psycopg as pg

logger = logging.getLogger(__name__)

SAMPLE_DATA = {
    "status": "ok",
    "data": {
        "time": {"iso": "2024-02-16T13:00:00+07:00"},
    },
}
CONNINFO = "host=localhost port=5432 dbname=test user=postgres password=postgres"
CREATE_TABLES = """
create table historical_pm25 (
    etl_ts timestamp,
    station_id bigint,
    pm25_value smallint
);
create table forecast_pm25 (
    etl_ts timestamp,
    station_id bigint,
    forecast_date date,
    forecast_pm25_avg smallint,
    forecast_pm25_max smallint,
    forecast_pm25_min smallint
);
create table stations (
    station_id bigint,
    station_name text,
    latitude float,
    longtitude float
);
"""
DROP_TABLES = """
drop table historical_pm25;
drop table forecast_pm25;
drop table stations;
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


@pytest.fixture(scope="module")
def postgres_session():
    with pg.connect(conninfo=CONNINFO) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLES)
        yield connection
        with connection.cursor() as cursor:
            cursor.execute(DROP_TABLES)

def test_postgres(postgres_session: pg.Connection):
    pass