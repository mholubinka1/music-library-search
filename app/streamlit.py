import logging.config
import sys
from logging import Logger, getLogger

from common.logging import APP_LOGGER_NAME, config
from common.settings import ApplicationSettings
from discogs.client import DiscogsClient
from startup import on_startup

logging.config.dictConfig(config)
logger: Logger = getLogger(APP_LOGGER_NAME)

logger.info("Starting music-library-search.")

settings: ApplicationSettings = on_startup(sys.argv)

client = DiscogsClient(
    username=settings.discogs.username, token=settings.discogs.access_token
)
test = client.get_collection_releases(releases_per_page=25)

print("here")
