import logging
import os

from metspa.interface import AEMETInterface
from metspa.utils import PACKAGE_DIRECTORY


class DataRequest:
    endpoint_fmt = "url_endpoint"

    def __init__(self) -> None:
        self.query_name = "query_name"
        self.endpoint = "full_endpoint"
        self._outdir = None
        self.logger = logging.getLogger("query")

    def get_from_api(self):
        api = AEMETInterface()
        self.logger.info(f"Calling AEMET API at {self.endpoint}")
        msg = api.get_api_msg(self.endpoint)

        return msg

    def run(self, refresh_from_api=False):
        if self.filename.exists() and not refresh_from_api:
            self.logger.info("Loading file from file")
            return self.load_from_file()
        else:
            msg = self.get_from_api()
            self.save(msg)
            return msg

    def load_from_file(self) -> str:
        with open(self.filename, "r") as f:
            msg = f.read()

        return msg

    @property
    def filename(self):
        return self.outdir / f"{self.query_name}.json"

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
    endpoint_fmt = (
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

        self.endpoint = self.endpoint_fmt.format(
            **{
                "start_year": self.start_year,
                "end_year": self.end_year,
                "station_id": self.station_id,
            }
        )

        self.outdir = outdir


class DailyDataRequest(DataRequest):
    endpoint_fmt = (
        "api/valores/climatologicos/diarios/datos"
        "/fechaini/{start_date}/fechafin/{end_date}/estacion/{station_id}"
    )

    def __init__(
        self, start_date: str, end_date: str, station_id: int, outdir=None
    ) -> None:
        super().__init__()

        self.start_date = start_date
        self.end_date = end_date
        self.station_id = station_id

        self.query_name = (
            f"daily_id{self.station_id}_s{self.start_date}_e{self.end_date}"
        )

        self.endpoint = self.endpoint_fmt.format(
            **{
                "start_date": self.start_date,
                "end_date": self.end_date,
                "station_id": self.station_id,
            }
        )

        self.outdir = outdir

    @staticmethod
    def _parse_date(date):
        raise NotImplementedError
