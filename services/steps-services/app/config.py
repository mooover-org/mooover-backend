import os
from configparser import ConfigParser

from corelib.domain.errors import NotFoundError


class AppConfig:
    """The configurations of the app at runtime"""
    __instance = None
    config = None
    auth0_config = None
    neo4j_config = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AppConfig, cls).__new__(cls)
            cls.config = cls._load_config()
            try:
                cls.auth0_config = cls.config["AUTH0"]
                cls.neo4j_config = cls.config["NEO4J"]
                try:
                    cls.neo4j_config["PASSWORD"] = os.environ["DB_PASSWORD"]
                except KeyError:
                    try:
                        with open(os.environ["DB_PASSWORD_FILE"]) as db_password_file:
                            cls.neo4j_config["PASSWORD"] = db_password_file.readline()
                    except KeyError:
                        raise NotFoundError(f"database password not found in the environment")
            except KeyError as e:
                raise NotFoundError(f"{e} config not found")
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
