import os
import shutil

import pytest

from metspa.interface import AEMETInterface
from metspa.utils import PACKAGE_DIRECTORY


@pytest.fixture
def station_id():
    "Generic station ID"
    return 3196


@pytest.fixture(scope="module")
def test_directory():
    test_dir = PACKAGE_DIRECTORY / "temp"
    os.makedirs(test_dir, exist_ok=True)
    yield test_dir
    shutil.rmtree(test_dir)


@pytest.mark.skip("Api call")
def test_api_msg(station_id, test_directory):

    msg = AEMETInterface().get_api_msg(
        endpoint=(
            "api/valores/climatologicos/inventarioestaciones/estaciones/"
            f"{station_id}"
        )
    )

    with open(test_directory / "test_api_msg.json", "w") as f:
        f.write(msg)
