from scripts.extract_from_aqicn import extract_current_timestamp
import datetime
from pytz import timezone
import logging

logger = logging.getLogger(__name__)

SAMPLE_DATA = {
    "status": "ok",
    "data": {
        "time": {"iso": "2024-02-16T13:00:00+07:00"},
    },
}


def test_extract_current_timestamp():
    timestamp = extract_current_timestamp(SAMPLE_DATA)
    logger.error(timestamp)
    expected_timestamp = datetime.datetime(2024, 2, 16, 13, 0, 0, tzinfo=timezone("Etc/GMT+7"))
    assert (timestamp.utcoffset().total_seconds() + expected_timestamp.utcoffset().total_seconds()) == 0 # quirky timezone
    assert timestamp.replace(tzinfo=None) == expected_timestamp.replace(tzinfo=None)
    wrong_timestamp = datetime.datetime(2024, 2, 16, 13, 0, 0, tzinfo=timezone("Etc/GMT+8"))
    assert not (timestamp.utcoffset().total_seconds() + wrong_timestamp.utcoffset().total_seconds()) == 0
