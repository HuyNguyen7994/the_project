sudo dnf update
sudo dnf install postgresql15.x86_64 postgresql15-server -y
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -i -u postgres psql -c "create table historical_pm25 (
    etl_ts timestamp with time zone,
    station_id bigint,
    city_name text,
    station_ts timestamp with time zone,
    pm25_value smallint
);
create index historical_pm25_idx on historical_pm25 (station_id, station_ts);
"