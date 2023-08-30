import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database.manager import session
from database.database_models import Game as Game_model
from queries.game.game_queries_update import insert_game, update_game_field
from models.models import Game_update, Update

router = APIRouter()

@router.post("/create_game", response_model=Update)
async def create_game(
        game: Game_model,
        session: AsyncSession = Depends(session.get_session)
):
    res = await insert_game(game, session)

    return {"status": res}

@router.post("/update_game", response_model=Update)
async def update_game(
        game_update: Game_update,
        session: AsyncSession = Depends(session.get_session)
):
    res = await update_game_field(game_update,
                                  session)

    return {"res": res}


