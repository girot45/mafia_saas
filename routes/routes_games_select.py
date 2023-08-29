import json
import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from game.game_queries_select import get_games_on_week_by_type,\
    get_games_by_user, get_current_games
from database.manager import session


router = APIRouter()

@router.post("/games_on_week_by_type")
async def games_on_week_by_type(
        user_id: int,
        type: str,
        session: AsyncSession = Depends(session.get_session)
):
    start_time = time.time()
    res = await get_games_on_week_by_type(user_id, type, session)

    res_dict = form_dict_for_messages(res)
    end_time = time.time()

    ex = end_time - start_time

    return json.dumps({
        "res": res,
        "res_dict": res_dict,
        "status": "True",
        "Error": "",
        "time": ex
    })


@router.post("/current_games")
async def current_games(
        user_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    start_time = time.time()
    res = await get_current_games(user_id, session)

    res_dict = form_dict_for_messages(res)
    end_time = time.time()

    ex = end_time - start_time

    return json.dumps({
        "res": res,
        "res_dict": res_dict,
        "status": "True",
        "Error": "",
        "time": ex
    })


@router.post("/games_by_user")
async def games_by_user(
        user_id: int,
        session: AsyncSession = Depends(session.get_session)
):
    res = await get_games_by_user(user_id, session)

    return json.dumps({"res":res})

def form_dict_for_messages(data):
    res_dict = {}
    for index, case in enumerate(data):
        num_of_players = case[6]
        max_players = case[7]
        if num_of_players is not None and max_players is not None and num_of_players < max_players:
            game_datetime_str = case[1] + ' ' + case[2]
            res_dict[index + 1] = [f"Время: {game_datetime_str}.\n"
                                   f"Адрес: {case[3]}\n"
                                   f"Цена: {case[8]}\n"
                                   f"Человек записанных на игру: "
                                   f"{case[6]}/{case[7]}\n\n",
                                   case[0], case[8]]
    return res_dict
