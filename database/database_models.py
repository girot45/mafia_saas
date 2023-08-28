from datetime import date
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    tg_id: int
    username: str
    user_fio: str
    user_photo: Optional[str]
    user_phone: str
    scores: Optional[int]
    balance: Optional[int]
    ref: Optional[str]

class Game(BaseModel):
    game_id: int
    game_date: date
    game_time_start: str
    game_time_end: str
    game_address: str
    type: str
    cost: int
    game_descr: str
    game_banner: str

class Marks(BaseModel):
    user_id: int
    mark: float
    count: int

class User_game(BaseModel):
    game_id: int
    user_id: int

class Types(BaseModel):
    type: str
    max_players: int
    min_players: int
