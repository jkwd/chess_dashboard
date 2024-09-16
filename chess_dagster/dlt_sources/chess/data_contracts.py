from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Accuracies(BaseModel):
    white: float
    black: float

class PlayerColor(BaseModel):
    rating: int
    result: str
    id: str = Field(alias="@id")
    username: str
    uuid: str
    

class PlayersGames(BaseModel):
    url: str
    pgn: str
    time_control: str
    end_time: datetime
    rated: bool
    accuracies: Optional[Accuracies] = None
    tcn: str
    uuid: str
    initial_setup: str
    fen: str
    time_class: str
    rules: str
    white: PlayerColor
    black: PlayerColor
    eco: str