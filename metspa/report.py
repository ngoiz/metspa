import logging

import pandas as pd

from metspa.postprocess import DailyDataProcess, MonthlyReport
from metspa.queries import DailyDataRequest
from metspa.utils import PACKAGE_DIRECTORY

logging.basicConfig(level=logging.INFO)

# end_date = datetime.now().isoformat()
end_date = "2022-12-26T00:00:00UTC"
start_date = "2022-09-01T00:00:00UTC"
station_id = "3434X"

json_data = DailyDataRequest(
    start_date=start_date, end_date=end_date, station_id=station_id
).run(refresh_from_api=False)

df = pd.read_json(json_data)
df = DailyDataProcess.tweak_data(df)
print(df.head())
monthly_report = MonthlyReport.create_from_daily_data(df)
print(monthly_report)

file_name = f"df_id{station_id}_s{start_date}_e{end_date}"

# save to feather
outdir = PACKAGE_DIRECTORY / "output"
df.reset_index().to_feather(outdir / f"daily_{file_name}.fea")

monthly_report.reset_index().to_feather(outdir / f"monthly_{file_name}.fea")
print("end")
