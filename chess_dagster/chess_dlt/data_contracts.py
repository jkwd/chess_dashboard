from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import datetime
from typing import ClassVar
from dlt.common.libs.pydantic import DltConfig


class Accuracies(BaseModel):
    white: Optional[float] = None
    black: Optional[float] = None

class PlayerColor(BaseModel):
    rating: int
    result: str
    id: str = Field(alias="@id")
    username: str
    uuid: str

class PlayersGamesBase(BaseModel):
    url: str
    rules: str
    pgn: Optional[str] = None # bughouse no pgn
    time_control: str
    end_time: datetime
    rated: bool
    accuracies: Optional[Accuracies] = None
    tcn: str
    uuid: str
    initial_setup: str
    fen: str
    time_class: str
    white: PlayerColor
    black: PlayerColor
    
    @field_validator('pgn', mode='after')  
    @classmethod
    def is_maybe_pgn(cls, pgn_value, info: ValidationInfo) -> str:
        rule = info.data.get('rules')
        
        if rule != 'bughouse' and pgn_value is None:
            raise ValueError('pgn is required for non-bughouse games')
        
        return pgn_value

class PlayersGames(PlayersGamesBase):
  dlt_config: ClassVar[DltConfig] = {"skip_nested_types": True}
