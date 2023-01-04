import argparse
import logging
import os
import shutil
import sys

import yaml

import metspa.temperatureloader as loader

PROGRAM_DIRECTORY = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__)) + "/../"
)


class MeteoSpa:
    def __init__(self):

        logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "function", help="Program function to run", choices=["fetch", "clean"]
        )

        self.number_of_arguments = 1  # in case new arguments are added

        options = parser.parse_args(
            sys.argv[1 : self.number_of_arguments + 1]
        )  # might need to change 2 to number of arguments if optionals included

        self.data = dict()
        self.data["program_directory"] = PROGRAM_DIRECTORY
        logging.info(f'Running program from {self.data["program_directory"]}')

        if not hasattr(self, options.function):
            logging.ERROR(f"Unrecognised command {options.function}")
            print(parser.print_help())

        self.__getattribute__(options.function)()

    def fetch(self):

        parser = argparse.ArgumentParser(description="Fetch data from AEMET")
        parser.add_argument("start_year", help="Initial year to fetch data", type=int)
        parser.add_argument("end_year", help="End year to fetch data", type=int)
        parser.add_argument("station_id", help="Meteo station ID")
        parser.add_argument(
            "-a", "--api", help="AEMET Open Data API Key or specifiy in config file"
        )
        parser.add_argument("-c", "--config", help="Configuration file")
        parser.add_argument("-o", "--output", help="Output directory to save data")
        # TODO: check parent for ArgumentParser to keep common inputs

        options = parser.parse_args(sys.argv[self.number_of_arguments + 1 :])

        API_KEY = get_api_key(options)

        self.data["api_key"] = API_KEY
        self.data["output_directory"] = get_output_directory(options)

        loader.extract_aemet_data(
            self.data, options.start_year, options.end_year, options.station_id
        )

    def clean(self):

        folders_to_delete = [
            os.path.join(self.data["program_directory"], "temp_output/")
        ]

        for folder in folders_to_delete:
            logging.info(f"Deleting {folder}")
            shutil.rmtree(folder)


def get_api_key(options):
    """
    Return API key from different input methods:

    1. Explicit key in command line through ``--api``

    2. Config file in command line thgough ``--config``

    3. Looking for the file ``<program_directory>/config.yaml``


    Args:
        options (Namespace): Namespace containing the parsed arguments

    Returns:
        str: API KEY
    """
    API_KEY = None

    if options.api:
        API_KEY = options.api
    elif options.config:
        data_dict = load_config_file(options.config)
        API_KEY = data_dict["api_key"]
    else:
        try:
            data_dict = load_config_file(PROGRAM_DIRECTORY + "/config.yaml")
        except FileNotFoundError:
            logging.critical("Unable to obtain an AEMET Open Data API Key")
            exit(1)
        else:
            API_KEY = data_dict["api_key"]

    return API_KEY


def get_output_directory(options):
    """
    Get output directory from program inputs and create directory if it doesn't exist

    1. From explicit setting through ``--output``

    2. From config file ``--config`` and entry ``output_directory``

    3. Defaults to ``<program_directory>/output/``

    Args:
        options (Namespace): Parser arguments namespace

    Return:
        str: output directory
    """
    if options.output:
        output_directory = options.output
    elif options.config:
        try:
            output_directory = load_config_file(options.config)["output_directory"]
        except KeyError:
            logging.warning(
                "Output directory ``output_directory`` not set in config file,"
                "reverting to default."
            )
            output_directory = f"{PROGRAM_DIRECTORY}/output/"
    else:
        output_directory = f"{PROGRAM_DIRECTORY}/output/"

    logging.info(f"Output directory set: {output_directory}")

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    return output_directory


def load_config_file(path_to_file):
    """
    Loads yaml file to list of dictionaries

    Args:
        path_to_file (str): Path to YAML file containing input of parameters.

    Returns:
        list: List of dictionaries
    """
    with open(path_to_file, "r") as yaml_file:
        out_dict = yaml.load(yaml_file, Loader=yaml.Loader)

    return out_dict


def main():
    MeteoSpa()
