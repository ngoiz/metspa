# Should replace processdata.py in the future
from dataclasses import dataclass

import pandas as pd


@dataclass
class Column:
    short_name: str
    long_name: str


@dataclass
class MonthlyReportColumn(Column):
    aggfunc_name: str
    parent_column: str

    @property
    def aggfunc(self):
        if self.parent_column and self.aggfunc_name:
            return pd.NamedAgg(column=self.parent_column, aggfunc=self.aggfunc_name)
        else:
            return None


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


class MonthlyReport:
    _monthly_report_aggregator_columns = [
        MonthlyReportColumn("prec", "Total Precipitation [mm]", "sum", "prec"),
        MonthlyReportColumn(
            "tmed", "Average of average daily temperature [C]", "mean", "tmed"
        ),
        MonthlyReportColumn(
            "tmin_med", "Average minimum daily temperature [C]", "mean", "tmin"
        ),
        MonthlyReportColumn("tmin_min", "Minimum daily temperature [C]", "min", "tmin"),
        MonthlyReportColumn(
            "tmax_med", "Average of daily maximum temperature [C]", "mean", "tmax"
        ),
        MonthlyReportColumn("tmax_max", "Maximum daily temperature [C]", "max", "tmax"),
        MonthlyReportColumn("velmedia", "Median wind speed [kph]", "mean", "velmedia"),
    ]
    _other_columns = [Column("prec_cumsum", "Accumulated Precipitation [mm]")]

    @classmethod
    @property
    def columns(cls):
        return cls._monthly_report_aggregator_columns + cls._other_columns

    @classmethod
    def create_from_daily_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.resample("M")
            .agg(
                **{
                    col.short_name: col.aggfunc
                    for col in cls._monthly_report_aggregator_columns
                }
            )
            .assign(prec_cumsum=lambda df_: df_.prec.cumsum())
            .sort_index(axis=1)
        )

    @classmethod
    def rename_columns(cls, df) -> pd.DataFrame:
        return df.rename(
            columns={col.short_name: col.long_name for col in cls.columns},
            index=lambda s: s.month_name(),
        ).rename_axis("Month")
