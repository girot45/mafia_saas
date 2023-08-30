from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import PendingRollbackError, SQLAlchemyError

from database.database import Game, User_game, Types
from database.manager import moscow_tz
from queries.utils import improve_data_output_view, create_log


async def get_games_on_week_by_type(user_id: int, game_type: str,
                                    session: AsyncSession):
    try:
        await create_log(user_id, 'get_games_on_week_by_type')
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
    except (
            PendingRollbackError, SQLAlchemyError, ConnectionError,
            ValueError, KeyError, AttributeError, TypeError) as e:
        await session.rollback()
        await create_log(user_id, 'get_games_on_week_by_type', error=str(e))


async def get_current_games(user_id: int, session: AsyncSession):
    try:
        await create_log(user_id, 'get_current_games')
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
    except (
        PendingRollbackError, SQLAlchemyError, ConnectionError,
        ValueError, KeyError, AttributeError, TypeError) as e:
        await session.rollback()
        await create_log(user_id, 'get_current_games', error=str(e))


async def get_games_by_user(user_id: int, session: AsyncSession):
    try:
        await create_log(user_id, 'get_games_by_user')
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
    except (PendingRollbackError, SQLAlchemyError, ConnectionError,
            ValueError,KeyError,AttributeError,TypeError) as e:
        await session.rollback()
        await create_log(user_id, 'get_games_by_user', error=str(e))