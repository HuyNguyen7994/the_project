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
create index historical_pm25_idx on historical_pm25 (station_id, etl_ts);
create index forecast_pm25_idx on forecast_pm25 (station_id, etl_ts);
create index forecast_pm25_idx_on_forecast_date on forecast_pm25 (station_id, forecast_date);
