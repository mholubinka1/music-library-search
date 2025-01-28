from argparse import ArgumentParser, Namespace
from typing import List

from common.settings import ApplicationSettings, ConfigLoader, validate_settings


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--config-file", type=str, required=True)
    parsed_args = parser.parse_args()
    return parsed_args


def on_startup(args: List[str]) -> ApplicationSettings:
    app_args = parse_args(args)
    config_loader = ConfigLoader(config_path=app_args.config_file)
    settings = config_loader.get_config()
    validate_settings(settings)
    return settings
