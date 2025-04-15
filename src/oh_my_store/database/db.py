from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncAttrs,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase
from oh_my_store.config import get_db_url


DATABASE_URL = get_db_url()
engine: AsyncEngine = create_async_engine(url=DATABASE_URL, echo=True)
async_session_factory = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if self.id == other.id:
            return True

        for column in inspect(self).attrs:
            if getattr(self, column, None) != getattr(other, column, None):
                return False
