import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, func

from database.database import Game
from database.database_models import Game as Game_model
from models.models import Game_update


async def update_game_field(
    game_update: Game_update,
    session: AsyncSession,
):
    try:
        async with session.begin():
            stmt = select(Game).filter(Game.game_id == game_update.game_id)
            result = await session.execute(stmt)
            game = result.scalars().first()

            if game:
                setattr(game, game_update.game_field,
                        game_update.new_value)
                await session.commit()
                return True
            else:
                return False
    except SQLAlchemyError:
        await session.rollback()
        return False


async def insert_game(game: Game_model, session: AsyncSession):
    try:
        new_game = Game(
            game_date=game.game_date,
            game_time_start=game.game_time_start,
            game_time_end=game.game_time_end,
            game_address=game.game_address,
            type=game.type,
            cost=game.cost,
            game_descr=game.game_descr,
            game_banner=game.game_banner,
            presenter=game.presenter
        )
        session.add(new_game)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        await session.rollback()
        return False
