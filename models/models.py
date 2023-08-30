from datetime import date
from typing import Optional
from pydantic import BaseModel


class Game_update(BaseModel):
    game_id: int
    game_field: str
    new_value: Optional[str]

class Profile(BaseModel):
    userame: str
    user_fio: str
    user_photo: str
    user_scores: int
    user_balance: int

class ProfileAnswer(BaseModel):
    user_profile: Profile
    status: bool


class Update(BaseModel):
    status: bool
