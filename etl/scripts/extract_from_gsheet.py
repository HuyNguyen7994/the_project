import os
import io
import requests
import psycopg
import pandas as pd
import datetime

LINK = os.getenv("LINK_TO_INPUT")
CONNINFO = os.getenv("POSTGRES_CONNINFO")

def download_csv(link) -> io.BytesIO:
    return io.BytesIO(requests.get(link).content)


def process_csv(file: bytes) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = ["booking_date", "room", "start_time", "end_time"]
    df["booking_date"] = pd.to_datetime(df["booking_date"], format="%d/%m/%Y")
    df["start_time"] = pd.to_datetime(df["start_time"], format="%H:%M").apply(
        lambda row: datetime.time(row.hour, row.minute)
    )
    df["end_time"] = pd.to_datetime(df["end_time"], format="%H:%M").apply(
        lambda row: datetime.time(row.hour, row.minute)
    )
    return df


def write_to_postgres(conninfo: str, df: pd.DataFrame):
    with psycopg.connect(conninfo=conninfo) as connection:
        with connection.cursor() as cursor:
            cursor.execute("truncate table bookings")
            with cursor.copy("copy bookings from STDIN with delimiter ',' csv") as copy:
                copy.write(df.to_csv(index=False, header=False))


def main():
    data = download_csv(LINK)
    df = process_csv(data)
    write_to_postgres(CONNINFO, df)

if __name__ == "__main__":
    main()
