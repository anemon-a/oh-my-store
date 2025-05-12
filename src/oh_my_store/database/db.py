from uuid import UUID as uuid
from uuid import uuid4

from sqlalchemy import UUID, inspect
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from oh_my_store.config import get_db_url

DATABASE_URL = get_db_url()
engine: AsyncEngine = create_async_engine(url=DATABASE_URL, echo=True)
async_session_factory = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if self.id == other.id:
            return True

        for column in inspect(self).attrs:
            if getattr(self, column.key, None) != getattr(other, column.key, None):
                return False

        return True
