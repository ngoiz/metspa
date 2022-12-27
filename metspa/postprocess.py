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

    @classmethod
    def tweak_data(cls, df: pd.DataFrame) -> pd.DataFrame:

        return df.assign(
            fecha=pd.to_datetime(df.fecha),
            # float columns
            **{
                col_name: df[col_name].str.replace(",", ".").astype("float16")
                for col_name in cls.float_columns
            },
            # sol=df.sol.astype('float16'),
            # time columns,
            **{
                col_name: pd.to_datetime(df[col_name].replace("Varias", None)).dt.time
                for col_name in cls.time_columns
            }
        ).set_index("fecha")

    @classmethod
    def monthly_report(cls, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby(df.index.month)
            .agg(
                prec=("prec", sum),
                tmed=pd.NamedAgg(column="tmed", aggfunc="mean"),
                tmin_min=("tmin", min),
                tmin_max=("tmin", max),
                tmax_min=("tmax", min),
                tmax_max=("tmax", max),
                velmedia_max=("velmedia", max),
                racha_max=("racha", max),
            )
            .assign(prec_cumsum=lambda df_: df_.prec.cumsum())
            .sort_index(axis=1)
        )
