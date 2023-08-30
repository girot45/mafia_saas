import json
import time
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from queries.game.game_queries_select import get_games_on_week_by_type,\
    get_games_by_user, get_current_games
from database.manager import session


router = APIRouter()

class GameResponse(BaseModel):
    res: dict
    status: bool
    Error: str

@router.post("/games_on_week_by_type", response_model=GameResponse)
async def games_on_week_by_type(
        user_id: int,
        type: str,
        session: AsyncSession = Depends(session.get_session)
):
    start_time = time.time()
    res = await get_games_on_week_by_type(user_id, type, session)
    end_time = time.time()

    ex = end_time - start_time

    return {
        "res": res,
        "status": True,
        "Error": "",
    }


@router.post("/current_games", response_model=GameResponse)
async def current_games(
        user_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    start_time = time.time()
    res = await get_current_games(user_id, session)
    end_time = time.time()

    ex = end_time - start_time

    return {
        "res": res,
        "status": "True",
        "Error": "",
    }


@router.post("/games_by_user", response_model=GameResponse)
async def games_by_user(
        user_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await get_games_by_user(user_id, session)

    return {"res": res, "status": True, "Error": ""}
