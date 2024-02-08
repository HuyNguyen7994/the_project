import sqlite3
from typing import Protocol, Optional, Type
from types import TracebackType
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


class DatabaseConnection(Protocol):
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        pass


class SqliteConnection(DatabaseConnection):
    connection: sqlite3.Connection

    def __init__(self, database: str):
        self.database = database

    def __enter__(self) -> sqlite3.Connection:
        logger.error(self.database)
        self.connection = sqlite3.connect(self.database)
        return self.connection

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        try:
            self.connection.commit()
        except Exception as e:
            logger.error(e)
        finally:
            self.connection.close()
