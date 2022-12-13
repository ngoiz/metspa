import logging
import os
from glob import glob

import numpy as np
import pandas as pd


def spanish_to_float(string_float_comma):
    try:
        return float(string_float_comma.replace(",", "."))
    except AttributeError:
        return string_float_comma
    except ValueError:
        return np.nan


def load_aggregated_data(directory):
    logging.info(f"Loading files from {directory}")
    json_data_files = glob(directory + "/climat*.json")
    logging.info(f"Found {len(json_data_files)} files to load...")
    frames = []
    for entry in json_data_files:
        frames.append(pd.read_json(entry))

    df = pd.concat(frames)

    logging.info("Dataframe loaded")

    return df


def split_date_time(df):
    logging.info("Converting date")
    df["year"] = df["fecha"].apply(lambda x: int(x.split("-")[0]))
    df["month"] = df["fecha"].apply(lambda x: int(x.split("-")[1]))
    df["day"] = df["fecha"].apply(lambda x: int(x.split("-")[2]))


def convert_floats(df):
    logging.info("Converting floats")
    float_columns = [
        "tmed",
        "tmin",
        "tmax",
        "prec",
        "dir",
        "velmedia",
        "racha",
        "presMax",
        "presMin",
    ]
    for col in float_columns:
        logging.debug(f"Processing column {col}")
        df[col] = df[col].apply(spanish_to_float)


def save_clean(df, idema, clean_directory):
    year_min = df.year.min()
    year_max = df.year.max()

    if not os.path.isdir(clean_directory):
        os.makedirs(clean_directory)

    outfile = clean_directory + f"/climat_{idema}_S{year_min}_E{year_max}.csv"
    df.to_csv(outfile)
    logging.info(f"Saved dataframe to {outfile}")


def clean_data_from_multiple_json(data_directory, output_directory, idema):

    df = load_aggregated_data(data_directory)

    split_date_time(df)

    convert_floats(df)

    save_clean(df, idema, output_directory)
