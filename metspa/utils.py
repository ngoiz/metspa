import os
from pathlib import Path

from dotenv import load_dotenv

import metspa.exceptions as exceptions

load_dotenv()

PACKAGE_DIRECTORY = Path(__file__).absolute().parent.parent


def read_environment_variable(env_variable_name):
    """Read selected environment variable"""
    env_var = os.getenv(env_variable_name)
    if not env_var:
        raise exceptions.EnvironmentVariableNotFoundError(env_variable_name)
    return env_var
