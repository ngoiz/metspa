# Should replace processdata.py in the future

import pandas as pd


class DailyDataProcess:
    float_columns = [
        "tmed",
        "tmin",
        "tmax",
        "prec",
        # "dir",
        "sol",
        "velmedia",
        "racha",
        "presMax",
        "presMin",
    ]
    time_columns = ["horatmin", "horatmax"]

    def tweak_data(self, df: pd.DataFrame) -> pd.DataFrame:

        return df.assign(
            fecha=pd.to_datetime(df.fecha),
            # float columns
            **{
                col_name: df[col_name].str.replace(",", ".").astype("float16")
                for col_name in self.float_columns
            },
            # sol=df.sol.astype('float16'),
            # time columns,
            **{
                col_name: pd.to_datetime(df[col_name].replace("Varias", None)).dt.time
                for col_name in self.time_columns
            }
        ).set_index("fecha")
