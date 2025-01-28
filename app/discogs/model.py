import logging.config
import re
from logging import Logger, getLogger
from typing import Dict, List, Set, Tuple

from common.logging import APP_LOGGER_NAME, config
from common.string_methods import is_null_or_empty

logging.config.dictConfig(config)
logger: Logger = getLogger(APP_LOGGER_NAME)

FORMAT_TYPES = ["Album", "Single", "Compilation", "EP", '12"']


def remove_discogs_artist_index(artist_name: str) -> str:
    return re.sub(r"\s\(\d+\)", "", artist_name)


def format_artists(artists: List[Dict]) -> Tuple[List[str], Set[str]]:
    display_artists: List[str] = []
    search_artists: Set[str] = set()
    for artist in artists:
        display_artists.append(remove_discogs_artist_index(artist["name"]))
        alt = artist["anv"]
        if not is_null_or_empty(alt):
            if ("The " + alt) == (artist["name"]):
                continue
            search_artists.add(remove_discogs_artist_index(alt))
    display_artists.sort()
    return display_artists, search_artists


def select_format(release: Dict, formats: List[Dict]) -> Tuple[str, Set[str]]:
    format_dict: Dict[str, Set[str]] = {}
    if len(formats) == 1:
        return formats[0]["name"]
    for f in formats:
        for type in FORMAT_TYPES:
            if type in f.get("descriptions", []):
                if type in format_dict.keys():
                    format_dict[type].add(f["name"])
                    continue
                format_dict[type] = {f["name"]}
    if len(format_dict.get("Album", [])) != 0:
        if len(format_dict.get("Album", [])) > 1:
            print("here1")
        return "Album", format_dict["Album"]
    if len(format_dict.get("Single", [])) != 0:
        if len(format_dict.get("Single", [])) > 1:
            print("here2")
        return "Single", format_dict["Single"]
    if len(format_dict.get("Compilation", [])) != 0:
        if len(format_dict.get("Compilation", [])) > 1:
            print("here3")
        return "Compilation", format_dict["Compilation"]
    if len(format_dict.get("EP", [])) != 0:
        if len(format_dict.get("EP", [])) > 1:
            print("here4")
        return "EP", format_dict["EP"]
    if len(format_dict.get('12"', [])) != 0:
        if len(format_dict.get('12"', [])) > 1:
            print("here5")
        return '12"', format_dict['12"']
    raise Exception("Format not found.")


class Release:
    master_id: int
    display_artists: List[str]
    search_artists: Set[str]
    title: str
    genre: Set[str]
    format: Set[str]
    cover_image_url: str

    def __init__(self, release: Dict) -> None:
        basic_info = release["basic_information"]
        if len(basic_info["artists"]) != 1:
            print("artist error")

        self.id = release["id"]
        self.date_added = release["date_added"]

        self.display_artists, self.search_artists = format_artists(
            basic_info["artists"]
        )
        self.title = basic_info["title"]
        self.genre = set(basic_info["genres"])
        self.genre.update(basic_info["styles"])
        self.year = basic_info["year"]
        self.formats = select_format(release, basic_info["formats"])
        self.cover_image_url = basic_info["cover_image"]
