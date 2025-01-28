import logging.config
from logging import Logger, getLogger
from typing import Any, Dict, List, Tuple, Union

import requests
from common.decorators import retry
from common.logging import APP_LOGGER_NAME, config
from discogs.model import Release

logging.config.dictConfig(config)
logger: Logger = getLogger(APP_LOGGER_NAME)


class DiscogsClient:
    _base_url = "https://api.discogs.com"
    _username: str
    _token: str

    def __init__(self, username: str, token: str) -> None:
        self._username = username
        self._token = token

    def get_collection_releases(self, releases_per_page: int) -> List[Any]:
        releases: List[Release] = []
        next_page_exists = True
        page = 1
        while next_page_exists:
            response_json = self.get_collection_releases_page(releases_per_page, page)
            next = response_json["pagination"]["urls"].get("next")
            page_releases = [Release(r) for r in response_json.get("releases")]
            releases.extend(page_releases)
            if not next:
                next_page_exists = False
                break
            page += 1
        return releases

    @retry()
    def get_collection_releases_page(
        self, releases_per_page: int, page: int = 1
    ) -> Tuple[int, List[Any]]:
        api_endpoint = (
            self._base_url + f"/users/{self._username}/collection/folders/0/releases"
        )
        params: Dict[str, Union[str, int]] = {
            "token": self._token,
            "per_page": releases_per_page,
            "page": page,
        }
        try:
            response = requests.get(
                url=api_endpoint,
                params=params,
            )
            response.raise_for_status()
            response_json = response.json()
            return response_json
        except Exception as e:
            if response.status_code != 200:
                response_json = response.json()
                raise Exception(response_json)
            raise Exception(f"Failed to get releases for page: {e}")
