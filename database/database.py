from sqlalchemy import Column, BIGINT, DateTime, String, Integer, \
    Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Types(Base):
    __tablename__ = "types"

    type = Column(String(length=255), primary_key=True,
                              index=True)
    max_players = Column(Integer)
    min_players = Column(Integer)


class Game(Base):
    __tablename__ = "game"

    game_id = Column(BIGINT, primary_key=True,index=True, autoincrement=True)
    game_date = Column(DateTime)
    game_time_start = Column(String(length=255))
    game_time_end = Column(String(length=255))
    game_address = Column(String(length=255))
    type = Column(String(length=255))
    cost = Column(Integer)
    game_descr = Column(Text)
    game_banner = Column(Text)
    presenter = Column(String(length=255))

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer)
    username = Column(String(length=255), index=True)
    user_fio = Column(String(length=255))
    user_photo = Column(Text, nullable=True, default=None)
    user_phone = Column(String(length=255))
    scores = Column(Integer, default=0)
    balance = Column(Integer, default=0)
    ref = Column(String, nullable=True, default=None)


class User_game(Base):
    __tablename__ = "user_game"

    game_id = Column(
        BIGINT,
        ForeignKey(
            "game.game_id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey(
            "user.user_id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        primary_key=True
    )


class Marks(Base):
    __tablename__ = "marks"

    user_id = Column(
        Integer,
        ForeignKey(
            "user.user_id",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    mark = Column(Float, index=True)
    count = Column(Integer)
