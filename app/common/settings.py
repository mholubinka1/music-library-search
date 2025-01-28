import logging.config
import sys
from dataclasses import dataclass
from logging import Logger, getLogger
from typing import Dict

import yaml
from common.logging import APP_LOGGER_NAME, config
from common.string_methods import is_null_or_empty

logging.config.dictConfig(config)
logger: Logger = getLogger(APP_LOGGER_NAME)


@dataclass
class DiscogsAuth:
    username: str
    access_token: str


class ApplicationSettings:
    def __init__(self, yaml_settings: Dict) -> None:
        self.discogs = DiscogsAuth(
            username=yaml_settings["discogs"]["username"],
            access_token=yaml_settings["discogs"]["token"],
        )


class ConfigLoader:
    _config: ApplicationSettings
    _path: str

    def __init__(self, config_path: str) -> None:
        self._path = config_path
        self._load_config()

    def get_config(self) -> ApplicationSettings:
        return self._config

    def _load_config(self) -> None:
        try:
            with open(self._path, "r") as file:
                settings = yaml.safe_load(file)
            logger.info(f"Successfully loaded settings from {self._path}")
            self._config = ApplicationSettings(settings)
        except Exception as e:
            logger.critical(
                f"Failed to load application settings from {self._path}: {e}"
            )
            sys.exit(1)


def validate_settings(settings: ApplicationSettings) -> None:
    if is_null_or_empty(settings.discogs.username):
        raise RuntimeError("A Discogs username must be provided.")
    if is_null_or_empty(settings.discogs.access_token):
        raise RuntimeError("A valid Personal Access Token must be provided.")
    return
