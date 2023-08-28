from datetime import date
from typing import Optional
from pydantic import BaseModel


class Game_update(BaseModel):
    game_id: int
    game_field: str
    new_value: Optional[str]