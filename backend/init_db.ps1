py -3.12 -m sqlite3 "database\prod.db" "CREATE TABLE IF NOT EXISTS checkin (
    participant_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    checkin_date DATE DEFAULT CURRENT_DATE
);"