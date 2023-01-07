# Should replace processdata.py in the future

import pandas as pd
from dataclasses import dataclass


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
        # TODO: create a dataclass for columns
        # @dataclass
        # Column:
        #   column.short_name
        #   column.long_name
        #   column.aggfunc
        #   column.parent_column
        #  
        # prec = Column("prec", "Total Precipitation [mm]", "sum", "prec")
        return (
            df.groupby(df.index.month)
            .agg(
                prec=("prec", sum),
                tmed=pd.NamedAgg(column="tmed", aggfunc="mean"),
                tmin_med=pd.NamedAgg(column="tmin", aggfunc="mean"),
                tmin_min=("tmin", min),
                tmax_med=pd.NamedAgg(column="tmax", aggfunc="mean"),
                tmax_max=("tmax", max),
                velmedia_max=("velmedia", max),
            )
            .assign(prec_cumsum=lambda df_: df_.prec.cumsum())
            .sort_index(axis=1)
        )
        
@dataclass
class Column:
    short_name: str
    long_name: str
    aggfunc_name: str
    parent_column: str
    
    @property
    def aggfunc(self):
        if self.parent_column and self.aggfunc_name:
            return pd.NamedAgg(column=self.parent_column, aggfunc=self.aggfunc_name)
        else:
            return None
    
monthly_report_columns = [
    Column("prec", "Total Precipitation [mm]", "sum", "prec"),
    Column("tmed", "Average of average daily temperature [C]", "mean", "tmed"),
    Column("tmin_med", "Average minimum daily temperature [C]", "mean", "tmin"),
    Column("tmin_min", "Minimum daily temperature [C]", "min", "tmin"),
    Column("tmax_med", "Average of daily maximum temperature [C]", "mean", "tmax"),
    Column("tmax_max", "Maximum daily temperature [C]", "max", "tmax"),
    Column("velmedia", "Median wind speed [kph]", "mean", "velmedia")
]