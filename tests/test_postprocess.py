import pandas as pd
import pytest

from metspa.postprocess import DailyDataProcess
from metspa.queries import DailyDataRequest
from metspa.utils import PACKAGE_DIRECTORY

resource_directory = PACKAGE_DIRECTORY / "tests/resources"


@pytest.fixture(scope="module")
def df():
    end_date = "2022-12-14T00:00:00UTC"
    start_date = "2022-09-01T00:00:00UTC"
    station_id = "3434X"

    json_data = DailyDataRequest(
        start_date=start_date,
        end_date=end_date,
        station_id=station_id,
        outdir=resource_directory,
    ).run(refresh_from_api=False)

    raw_df = pd.read_json(json_data)

    return DailyDataProcess().tweak_data(raw_df)


def test_daily_numeric_column_processing(df: pd.DataFrame):

    cols_as_float16 = set(df.select_dtypes(include="float16").columns)
    target_cols = set(DailyDataProcess.float_columns)
    unformated_columns = target_cols - cols_as_float16

    assert (
        len(unformated_columns) == 0
    ), f"Some columns were not properly formatted {unformated_columns}"
