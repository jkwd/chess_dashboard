from typing import Any, Optional, Generator, List, Dict
import logging

import dlt
from dlt.sources.helpers import requests

from .data_contracts import PlayersGames

# Create a logger
logger = logging.getLogger('dlt')

# Set the log level
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('/data/dlt.log')

# Add the handler to the logger
logger.addHandler(handler)

@dlt.source(name="chess")
def source(username: str):
    return player_games(username=username)

@dlt.resource(write_disposition="replace", columns=PlayersGames)
def player_games(username: str) -> Generator[Any, Any, Any]:
    """
    Yields player's `username` games.
    Args:
        username: str: Player username to retrieve games for.
    Yields:
        Generator[Any, Any, Any]: A generator that return a list of games for a player.
    """
    
    # get archives in parallel by decorating the http request with defer
    @dlt.defer
    def _get_archive(url: str):
        logger.warning(f"Getting archive from {url}")
        try:
            games = requests.get(url).json().get("games", [])
            return games  # type: ignore
        
        except requests.HTTPError as http_err:
            # sometimes archives are not available and the error seems to be permanent
            if http_err.response.status_code == 404:
                return []
            raise
        except Exception as err:
            logger.error(f"Unexpected error: {err}")
            raise
    
    archives = player_archives(username)
    
    for url in archives:
        # the `url` format is https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}
        
        # get the filtered archive
        yield _get_archive(url)
        

@dlt.resource()
def player_archives(username: str) -> Generator[List[Dict[str, Any]], Any, Any]:
    """
    Yields url to game archives for a specified player username.
    Args:
        username: str: Player username to retrieve archives for.
    Yields:
        Generator[List[Dict[str, Any]], Any, Any]: List of player archive data.
    """

    data = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives")
    yield data.json().get("archives", [])