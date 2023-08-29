from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import pytz


host = "92.53.115.237"
user = "gen_user"
password = "WFVSZ[XD$BK2tH"
database = "default_db"

DATABASE_URL = f"mysql+aiomysql://{user}:{password}@{host}/{database}"

moscow_tz = pytz.timezone('Europe/Moscow')


class Database:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True)

    async def get_session(self) -> AsyncSession:
        async_session = sessionmaker(bind=self.engine, class_=AsyncSession)
        async with async_session() as session:
            yield session


session = Database(DATABASE_URL)
