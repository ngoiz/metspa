import os

import pytest

from metspa.interface import AEMETInterface
from metspa.utils import PACKAGE_DIRECTORY


@pytest.fixture
def station_id():
    "Generic station ID"
    return 3196


def test_api_msg(station_id):
    test_dir = PACKAGE_DIRECTORY / "temp"
    os.makedirs(test_dir, exist_ok=True)

    msg = AEMETInterface().get_api_msg(
        endpoint=(
            "api/valores/climatologicos/inventarioestaciones/estaciones/"
            f"{station_id}"
        )
    )

    with open(test_dir / "test_api_msg.json", "wb") as f:
        f.write(msg)
