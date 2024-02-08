from . workers.database import SqliteConnection
from pathlib import Path
import os
import sqlite3
import pytest

@pytest.fixture(scope="function")
def temp_db() -> sqlite3.Connection:
    try:
        path_to_database = str(Path(__file__).parent.parent.parent / "database" / "temp.db")
        with SqliteConnection(path_to_database) as conn:
            yield conn
    finally:
        os.remove(path_to_database)


def test_sqlite_connection():
    with SqliteConnection(":memory:") as conn:
        cursor = conn.cursor()
        cursor.execute("select 1")
        assert cursor.fetchone() == (1,)

def test_sqlite_connection_disk(temp_db: sqlite3.Connection):
    cursor = temp_db.cursor()
    cursor.execute("create table test (id serial, name text)")
    cursor.execute("insert into test (id, name) values (1, 'foo'), (2, 'bar')")
    cursor.execute("select * from test")
    assert cursor.fetchall() == [(1, "foo"), (2, "bar")]
    cursor.execute("insert into test (id, name) values (3, 'baz')")
    cursor.execute("select count(*) from test")
    assert cursor.fetchone() == (3,)

