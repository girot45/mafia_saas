import json
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import ProfileAnswer, Update
from queries.user.user_queries import insert_user, insert_user_game, \
    get_users_by_game, get_user_profile, add_games_to_subscription, \
    subtract_game, deregister_game, make_a_mark, \
    get_list_of_players_by_rank
from database.manager import session
from database.database_models import User, User_game

router = APIRouter()

@router.post("/reg_user", response_model=Update)
async def write_user_to_db(user: User, session: AsyncSession = Depends(
    session.get_session)):
    res = await insert_user(user, session)

    return {
        "status": res,
    }


@router.post("/reg_user_game", response_model=Update)
async def reg_user_game(
        user_game: User_game,
        session: AsyncSession = Depends(session.get_session)
):
    res = await insert_user_game(user_game, session)
    return {
        "res": res,
    }


@router.delete("/unrecord", response_model=Update)
async def unrecord(
        user_game: User_game,
        session: AsyncSession = Depends(session.get_session)
):
    res = await deregister_game(user_game, session)
    return {
        "res": res,
    }


class UsersGame(BaseModel):
    users_photo: List
    users_info: List


@router.post("/users_by_game", response_model=UsersGame)
async def users_by_game(
        user_id: int,
        game_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await get_users_by_game(user_id, game_id, session)
    users_photo, users_info = res
    return {"users_photo": users_photo, "users_info": users_info}




@router.post("/get_profile", response_model=ProfileAnswer)
async def get_profile(user_id: int, session: AsyncSession = Depends(
    session.get_session)):
    res = await get_user_profile(user_id, session)
    return res


@router.post("/top_up_subscription", response_model=Update)
async def top_up_subscription(
        user_id: int,
        count_games: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await add_games_to_subscription(user_id, count_games, session)
    return {"res": res}


@router.post("/spend_game", response_model=Update)
async def spend_game(
        user_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await subtract_game(user_id, session)
    return res


@router.post("/mark_player", response_model=Update)
async def mark_player(
        username: str,
        mark: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await make_a_mark(username, mark, session)
    if res["status"] in [1,2]:
        return {"status": True}
    else:
        return {"status": False}

@router.get("/players_by_rank")
async def players_by_rank(
        user_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = get_list_of_players_by_rank(user_id, session)