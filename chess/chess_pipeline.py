"""A source loading player profiles and games from chess.com api"""

from typing import Any, Callable, Dict, Iterator, List, Sequence

import dlt
from dlt.common import pendulum
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
from dlt.sources.helpers import requests

from pipeline_helper import get_path_with_retry, get_url_with_retry, validate_month_string
from settings import UNOFFICIAL_CHESS_API_URL

import duckdb

@dlt.source(name="chess")
def source(
    username: str, start_month: str = None, end_month: str = None
) -> Sequence[DltResource]:
    """
    A dlt source for the chess.com api. It groups several resources (in this case chess.com API endpoints) containing
    various types of data: user profiles or chess match results
    Args:
        username (str): Username for which to get the data.
        start_month (str, optional): Filters out all the matches happening before `start_month`. Defaults to None.
        end_month (str, optional): Filters out all the matches happening after `end_month`. Defaults to None.
    Returns:
        Sequence[DltResource]: A sequence of resources that can be selected from including player_profile,
        player_archives, player_games
    """
    return (
        player_profile(username),
        player_archives(username),
        player_games(username, start_month=start_month, end_month=end_month),
    )


@dlt.resource(
    write_disposition="replace",
    columns={
        "last_online": {"data_type": "timestamp"},
        "joined": {"data_type": "timestamp"},
    },
)
def player_profile(username: str) -> TDataItem:
    """
    Yields player profile.
    Args:
        username (str): Username to retrieve profiles for.
    Yields:
        TDataItem: Player profiles data.
    """

    # get archives in parallel by decorating the http request with defer
    @dlt.defer
    def _get_profile(username: str) -> TDataItem:
        return get_path_with_retry(f"player/{username}")


    yield _get_profile(username)


@dlt.resource(write_disposition="replace", selected=False)
def player_archives(username: str) -> Iterator[List[TDataItem]]:
    """
    Yields url to game archives for specified username.
    Args:
        players (str): Username to retrieve archives for.
    Yields:
        Iterator[List[TDataItem]]: An iterator over list of player archive data.
    """
    data = get_path_with_retry(f"player/{username}/games/archives")
    yield data.get("archives", [])


@dlt.resource(
    write_disposition="replace", columns={"end_time": {"data_type": "timestamp"}}
)
def player_games(
    username: str, start_month: str = None, end_month: str = None
) -> Iterator[Callable[[], List[TDataItem]]]:
    """
    Yields `players` games that happened between `start_month` and `end_month`.
    Args:
        players (List[str]): List of player usernames to retrieve games for.
        start_month (str, optional): The starting month in the format "YYYY/MM". Defaults to None.
        end_month (str, optional): The ending month in the format "YYYY/MM". Defaults to None.
    Yields:
        Iterator[Callable[[], List[TDataItem]]]: An iterator over callables that return a list of games for each player.
    """  # do a simple validation to prevent common mistakes in month format
    validate_month_string(start_month)
    validate_month_string(end_month)

    # get a list of already checked archives
    # from your point of view, the state is python dictionary that will have the same content the next time this function is called
    checked_archives = dlt.current.resource_state().setdefault("archives", [])
    # get player archives, note that you can call the resource like any other function and just iterate it like a list
    archives = player_archives(username)

    # get archives in parallel by decorating the http request with defer
    @dlt.defer
    def _get_archive(url: str) -> List[TDataItem]:
        print(f"Getting archive from {url}")
        try:
            games = get_url_with_retry(url).get("games", [])
            return games  # type: ignore
        except requests.HTTPError as http_err:
            # sometimes archives are not available and the error seems to be permanent
            if http_err.response.status_code == 404:
                return []
            raise

    # enumerate the archives
    for url in archives:
        # the `url` format is https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}
        if start_month and url[-7:] < start_month:
            continue
        if end_month and url[-7:] > end_month:
            continue
        # do not download archive again
        if url in checked_archives:
            continue
        checked_archives.append(url)
        # get the filtered archive
        yield _get_archive(url)


def run_pipeline(db, username, start_month=None, end_month=None):
    pipeline = dlt.pipeline(
        pipeline_name="chess_pipeline", # Use a custom name if desired
        destination=dlt.destinations.duckdb(db),
        dataset_name="chess_data", # Use a custom name if desired
    )

    data = source(username, start_month=start_month,end_month=end_month)

    info = pipeline.run(data)
    # print the information on data that was loaded
    print(info)