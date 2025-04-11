from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncAttrs,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase

# URL = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
URL = "sqlite+aiosqlite:///db.db"
engine: AsyncEngine = create_async_engine(url=URL, echo=True)
async_session_factory = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError

        if self.id == other.id:
            return True

        for column in inspect(self).attrs:
            if getattr(self, column, None) != getattr(other, column, None):
                return False
