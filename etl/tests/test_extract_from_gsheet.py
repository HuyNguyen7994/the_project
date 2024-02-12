from scripts.extract_from_gsheet import main, process_csv, write_to_postgres
from pathlib import Path
import pytest
import pytest_mock
from logging import getLogger
import psycopg as pg
import io

logger = getLogger(__name__)
CONNINFO = "host=localhost port=5432 dbname=test user=postgres password=postgres"


@pytest.fixture(scope="session")
def sample_folder() -> Path:
    return Path(__file__).parent / "test_extract_from_gsheet"


def test_process_csv(sample_folder: Path):
    with open(sample_folder / "sample_data.csv", "rb") as file:
        df = process_csv(file)
    logger.error(df)
    assert len(df) == 6
    assert df.columns.to_list() == ["booking_date", "room", "start_time", "end_time"]


def test_insert_database(sample_folder: Path):
    with open(sample_folder / "sample_data.csv", "rb") as file:
        df = process_csv(file)
    write_to_postgres(CONNINFO, df)
    with pg.connect(conninfo=CONNINFO) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from bookings")
            logger.error("Try writing data for the first time")
            assert cursor.fetchone() == (6,)
    write_to_postgres(CONNINFO, df)
    with pg.connect(conninfo=CONNINFO) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select count(*) from bookings")
            logger.error("Try writing data for the second time")
            assert cursor.fetchone() == (6,)

def test_main(sample_folder: Path, mocker: pytest_mock.MockerFixture):
    mocker.patch(
        "scripts.extract_from_gsheet.CONNINFO",
        CONNINFO,
    )
    with open(sample_folder / "sample_data.csv", "rb") as file:
        data = io.BytesIO(file.read())
    mocker.patch(
        "scripts.extract_from_gsheet.download_csv",
        return_value=data,
    )
    main()
    assert True
