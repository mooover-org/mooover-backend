import os
from configparser import ConfigParser

from app.domain.errors import NotFoundError


class AppConfig:
    """The configurations of the app at runtime"""
    __instance = None
    __config = None
    auth0_config = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AppConfig, cls).__new__(cls)
            cls.__config = cls._load_config()
            try:
                cls.auth0_config = cls.__config["AUTH0"]
            except KeyError:
                raise NotFoundError("auth0 config not found")
        return cls.__instance

    @staticmethod
    def _load_config() -> ConfigParser:
        """
        Loads the .config file from the root of the project.

        :return: the config
        """
        env = os.getenv("ENV", ".config")
        if env == ".config":
            config = ConfigParser()
            config.read([".config", ".test.config"])
            return config
        raise NotFoundError("config file not found")
