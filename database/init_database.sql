create table historical_pm25 (
    etl_ts timestamp with time zone,
    station_id bigint,
    station_name text,
    station_ts timestamp with time zone,
    pm25_value smallint
);
create index historical_pm25_idx on historical_pm25 (station_id, station_ts);
