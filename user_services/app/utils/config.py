import os
from configparser import ConfigParser

from app.domain.errors import NotFoundError


def load_config() -> ConfigParser:
    """
    Loads the .config file from the root of the project.

    :return: the config
    """
    env = os.getenv("ENV", ".config")
    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        return config
    raise NotFoundError("config file not found")
