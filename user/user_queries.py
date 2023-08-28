from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import User_game, User, Marks
from sqlalchemy import select, func


async def insert_user_game(
        user_game: User_game,
        session: AsyncSession
):
    try:
        new_user_game = User_game(game_id=user_game.game_id,
                                  user_id=user_game.user_id)
        session.add(new_user_game)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        return False


async def insert_user(user: User, session: AsyncSession):
    try:
        if user.user_photo == "attachment_url":
            photo = None
        else:
            photo = user.user_photo

        new_user = User(
            user_id=user.user_id,
            tg_id=user.tg_id,
            username=user.username,
            user_fio=user.user_fio,
            user_photo=photo,
            user_phone=user.user_phone
        )

        session.add(new_user)
        await session.commit()

        return True
    except SQLAlchemyError:
        await session.rollback()
        return False


async def get_users_by_game(
        game_id: int,
        session: AsyncSession
):
    try:
        async with session.begin():
            stmt = (
                select(User)
                .join(User_game)
                .where(User_game.game_id == game_id)
            )
            result = await session.execute(stmt)

            players = result.scalars().all()
            users = [{
                "userame": user.username,
                "user_fio": user.user_fio,
                "user_photo": user.user_photo,
                "user_scores": user.scores,
                "user_balance": user.balance,

            } for user in players]

            return users
    except SQLAlchemyError:
        await session.rollback()
        return False


async def get_user_profile(user_id: int, session: AsyncSession):
    try:
        async with session.begin():
            stmt = (
                select(User)
                .where(User.user_id == user_id)
            )
            result = await session.execute(stmt)
            user_profile = result.scalars().first()
            if user_profile:
                return {"userame": user_profile.username,
                        "user_fio": user_profile.user_fio,
                        "user_photo": user_profile.user_photo,
                        "user_scores": user_profile.scores,
                        "user_balance": user_profile.balance,
                        "status": True}
    except SQLAlchemyError:
        await session.rollback()
        return {"user_profile": None, "status": False}


async def add_games_to_subscription(
        user_id: int,
        games_quantity: int,
        session: AsyncSession
):
    try:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one()

        if user:
            # Assuming you have a field for tracking games subscription
            user.balance += games_quantity
            await session.commit()
            return True
        else:
            return False
    except SQLAlchemyError:
        await session.rollback()
        return False


async def subtract_game(user_id: int, session: AsyncSession):
    try:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one()

        if user and user.balance >= 1:
            user.balance -= 1
            await session.commit()
            return True
        else:
            return False
    except SQLAlchemyError:
        await session.rollback()
        return False


async def deregister_game(
        user_game: User_game,
        session: AsyncSession
):
    try:
        stmt = (
            select(User_game)
            .filter(User_game.user_id == user_game.user_id,
                    User_game.game_id == user_game.game_id)
        )
        result = await session.execute(stmt)
        user_game = result.scalar_one()

        if user_game:
            await session.delete(user_game)
            await session.commit()
            return True
        else:
            return False
    except SQLAlchemyError:
        await session.rollback()
        return False


async def make_a_mark(
        username: str,
        mark: int, session: AsyncSession
):
    try:
        async with session.begin():
            user_query = (
                select(User.user_id)
                .where(User.username == username)
            )
            user_id = await session.execute(user_query)
            res = user_id.scalar_one_or_none()

            if res:
                mark_query = (
                    select(Marks)
                    .filter(Marks.user_id == user_id)
                )
                mark_row = await session.execute(mark_query)
                mark_data = mark_row.scalar_one_or_none()

                if mark_data:
                    count = mark_data.count + 1
                    mark = (mark_data.mark + mark) / count

                    mark_data.mark = mark
                    mark_data.count = count
                else:
                    new_mark = Marks(
                        user_id=user_id,
                        mark=mark,
                        count=1
                    )
                    session.add(new_mark)
            else:
                return {"status": 3}

            await session.commit()

            if mark_data:
                return {"status": 1}
            else:
                return {"status": 2}

    except SQLAlchemyError:
        await session.rollback()
        return {"status": 0}


async def get_list_of_players_by_rank(
        user_id: int,
        session: AsyncSession
):
    pass