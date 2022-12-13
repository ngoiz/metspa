import pytest

from metspa.queries import MonthlyDataRequest


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
