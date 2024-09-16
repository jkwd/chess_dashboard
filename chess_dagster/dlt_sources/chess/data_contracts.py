from pydantic import BaseModel
from datetime import datetime

class PlayersGames(BaseModel):
    end_time: datetime
    url: str
    pgn: str
    time_control: str
    rated: bool
    accuracies__white: float
    accuracies__black: float
    tcn: str
    uuid: str
    initial_setup: str
    fen: str
    time_class: str
    rules: str
    white__rating: int
    white__result: str
    white__aid: str
    white__username: str
    white__uuid: str
    black__rating: int
    black__result: str
    black__aid: str
    black__username: str
    black__uuid: str