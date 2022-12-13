import logging
import os

from metspa.interface import AEMETInterface
from metspa.utils import PACKAGE_DIRECTORY


class DataRequest:
    endpoint = "url_endpoint"

    def __init__(self) -> None:
        self.query_name = "query_name"
        self._outdir = None
        self.logger = logging.getLogger("query")

    def get_from_api():
        return "api_msg"

    def run(self):
        if self.filename.exists():
            self.logger.info("Loading file from file")
            return self.load_from_file()
        else:
            return self.get_from_api()

    def load_from_file(self) -> str:
        with open(self.filename, "r") as f:
            msg = f.read()

        return msg

    @property
    def filename(self):
        return self.outdir / f"{self.query_name}.txt"

    @property
    def outdir(self):
        return self._outdir

    @outdir.setter
    def outdir(self, path):
        if path is None:
            self._outdir = PACKAGE_DIRECTORY / "output"

    def save(self, msg):
        if not self.outdir.is_dir():
            os.makedirs(self.outdir, exist_ok=True)

        with open(self.filename, "w") as fid:
            fid.write(msg)


class MonthlyDataRequest(DataRequest):
    endpoint = (
        "api/valores/climatologicos/mensualesanuales/datos/"
        "anioini/{start_year}/aniofin/{end_year}/estacion/{station_id}"
    )

    def __init__(
        self, start_year: int, end_year: int, station_id: int, outdir=None
    ) -> None:
        super().__init__()

        self.start_year = start_year
        self.end_year = end_year

        self.station_id = station_id

        self.query_name = (
            f"monthly_id{self.station_id}_s{self.start_year}_e{self.end_year}"
        )

        self.outdir = outdir

    def get_from_api(self):
        api = AEMETInterface()

        msg = api.get_api_msg(
            endpoint=self.endpoint.format(
                **{
                    "start_year": self.start_year,
                    "end_year": self.end_year,
                    "station_id": self.station_id,
                }
            )
        )

        return msg
