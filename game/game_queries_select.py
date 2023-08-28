from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import PendingRollbackError

from database.database import Game, User_game, Types
from database.manager import moscow_tz
from database.utils import improve_data_output_view


async def get_games_on_week_by_type(game_type, session: AsyncSession):
    try:
        current_date = datetime.now(moscow_tz).date()
        future_date = current_date + timedelta(days=7)

        stmt = (
            select(Game, func.count(User_game.game_id),
                   Types.max_players)
            .outerjoin(User_game, Game.game_id == User_game.game_id)
            .outerjoin(Types, Game.type == Types.type)
            .filter(Types.type == game_type)
            .filter(Game.game_date.between(current_date, future_date))
            .group_by(Game.game_id)
        )

        result = await session.execute(stmt)
        mafia_games = result.fetchall()

        return improve_data_output_view(mafia_games)
    except PendingRollbackError:
        await session.rollback()


async def get_current_games(session: AsyncSession):
    try:
        current_date = datetime.now(moscow_tz).date()
        stmt = (
            select(Game, func.count(User_game.game_id),
                          Types.max_players)
            .outerjoin(User_game, Game.game_id == User_game.game_id)
            .outerjoin(Types, Game.type == Types.type)
            .filter(Game.game_date == current_date)
            .group_by(Game.game_id)
        )
        result = await session.execute(stmt)
        mafia_games = result.fetchall()

        return improve_data_output_view(mafia_games)
    except PendingRollbackError:
        await session.rollback()


async def get_games_by_user(user_id: int, session: AsyncSession):
    try:
        current_date = datetime.now(moscow_tz).date()
        stmt = (
            select(Game, func.count(User_game.game_id),
                          Types.max_players)
            .outerjoin(User_game, Game.game_id == User_game.game_id)
            .outerjoin(Types, Game.type == Types.type)
            .filter(Game.game_date >= current_date)
            .filter(User_game.user_id == user_id)
            .group_by(Game.game_id)
        )
        result = await session.execute(stmt)
        mafia_games = result.fetchall()

        return improve_data_output_view(mafia_games)
    except PendingRollbackError:
        await session.rollback()