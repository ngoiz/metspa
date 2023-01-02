import logging

import pandas as pd

from metspa.outmail import EmailSender
from metspa.postprocess import DailyDataProcess
from metspa.queries import DailyDataRequest
from metspa.utils import PACKAGE_DIRECTORY

logging.basicConfig(level=logging.INFO)

# end_date = datetime.now().isoformat()
end_date = "2022-12-26T00:00:00UTC"
start_date = "2022-09-01T00:00:00UTC"
station_id = "3434X"

# Llanes
end_date = "2023-01-01T00:00:00UTC"
start_date = "2022-09-01T00:00:00UTC"
station_id = "1183X"

json_data = DailyDataRequest(
    start_date=start_date, end_date=end_date, station_id=station_id
).run(refresh_from_api=False)

df = pd.read_json(json_data)
df = DailyDataProcess.tweak_data(df)
print(df.head())
monthly_report = DailyDataProcess.monthly_report(df)
print(monthly_report.head())

file_name = f"df_id{station_id}_s{start_date}_e{end_date}"

# save to feather
outdir = PACKAGE_DIRECTORY / "output"
df.reset_index().to_feather(outdir / f"daily_{file_name}.fea")

monthly_report.reset_index().to_feather(outdir / f"monthly_{file_name}.fea")

station_name = df.nombre.iloc[0]
province = df.provincia.iloc[0]

# Format pandas to string
out = monthly_report.to_markdown(
    index=True, tablefmt="pipe", colalign=["center"] * len(monthly_report.columns)
)
out = out.split("\n")
out.pop(1)
out = "\n".join(out)


message = f"""
Hi Norberto,

The monthly meteorological summary at {station_name} in {province} is provided below.

Data from {start_date} to {end_date}.

{out}"""

print(message)

sender = EmailSender()
# sender("norbertogoizveta@me.com", message)
sender.generate_html_message(
    "norbertogoizveta@me.com",
    monthly_report,
    station_name=station_name,
    province=province,
    start_date=start_date,
    end_date=end_date,
)
print("end")
