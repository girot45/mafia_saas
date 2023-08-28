import json
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.manager import session
from database.database_models import Game as Game_model
from game.game_queries_update import insert_game, update_game_field
from models.game_models import Game_update

router = APIRouter()

@router.post("/create_game")
async def create_game(
        game: Game_model,
        session: AsyncSession = Depends(session.get_session)
):
    res = await insert_game(game, session)

    return json.dumps({"status": res})

@router.post("/update_game")
async def update_game(
        game_update: Game_update,
        session: AsyncSession = Depends(session.get_session)
):
    res = await update_game_field(game_update,
                                  session)

    return {"res": res}