import pytest

from metspa.queries import DailyDataRequest, MonthlyDataRequest


@pytest.fixture
def station_id():
    "Generic station ID"
    return 3196


def test_get_monthly_data(station_id):
    start_year = 2020
    end_year = 2020

    MonthlyDataRequest(
        start_year=start_year, end_year=end_year, station_id=station_id
    ).run()


def test_get_daily_data(station_id):

    start_date = "2020-01-01T00:00:00UTC"
    end_date = "2021-01-01T00:00:00UTC"

    DailyDataRequest(
        start_date=start_date, end_date=end_date, station_id=station_id
    ).run(refresh_from_api=True)
