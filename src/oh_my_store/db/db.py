import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from oh_my_store.db.models.models import Base

URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(url=URL, echo=True)
async_session = async_sessionmaker(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_tables() -> None:
    """Создание всех таблиц в базе данных"""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """Удаление всех таблиц из базы данных"""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def main():
    await drop_tables()
    await create_tables()


if __name__ == "__main__":
    asyncio.run(main())
