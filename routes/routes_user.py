import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from user.user_queries import insert_user, insert_user_game, \
    get_users_by_game, get_user_profile, add_games_to_subscription, \
    subtract_game, deregister_game, make_a_mark
from database.manager import session
from database.database_models import User, User_game


router = APIRouter()

@router.post("/reg_user")
async def write_user_to_db(user: User, session: AsyncSession = Depends(
    session.get_session)):
    res = await insert_user(user, session)

    return json.dumps({
        "res": res,
        "Error": "",
    })


@router.post("/reg_user_game")
async def reg_user_game(
        user_game: User_game,
        session: AsyncSession = Depends(session.get_session)
):
    res = await insert_user_game(user_game, session)
    return json.dumps({
        "res": res,
        "Error": "",
    })


@router.delete("/unrecord")
async def unrecord(
        user_game: User_game,
        session: AsyncSession = Depends(session.get_session)
):
    res = await deregister_game(user_game, session)
    return res


@router.get("/users_by_game")
async def users_by_game(
        game_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await get_users_by_game(game_id, session)
    return json.dumps(res)


@router.get("/get_profile")
async def get_profile(user_id: int, session: AsyncSession = Depends(
    session.get_session)):
    res = await get_user_profile(user_id, session)
    return res


@router.post("/top_up_subscription")
async def top_up_subscription(
        user_id: int,
        count_games: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await add_games_to_subscription(user_id, count_games, session)
    return json.dumps({"res": res})


@router.post("/spend_game")
async def spend_game(
        user_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await subtract_game(user_id, session)
    return res


@router.post("/mark_player")
async def mark_player(
        username: str,
        mark: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await make_a_mark(username, mark, session)
    if res["status"] in [1,2]:
        return json.dumps({"status": True})
    else:
        return json.dumps({"status": False})

@router.get("/players_by_rank")
async def players_by_rank(
        user_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = get_list_of_players_by_rank(user_id, session)