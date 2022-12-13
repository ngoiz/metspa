import logging

import pandas as pd

from metspa.queries import DailyDataRequest

logging.basicConfig(level=logging.INFO)

# end_date = datetime.now().isoformat()
end_date = "2022-12-12T00:00:00UTC"
start_date = "2022-09-01T00:00:00UTC"
station_id = "3434X"

json_data = DailyDataRequest(
    start_date=start_date, end_date=end_date, station_id=station_id
).run(refresh_from_api=False)

df = pd.read_json(json_data)
print(df.head())
print("end")
