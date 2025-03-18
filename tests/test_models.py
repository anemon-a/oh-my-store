from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


@pytest.fixture(autouse=True)
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async_session = async_sessionmaker(bind=engine)
    session: AsyncSession = async_session()
    yield session
    await session.close()


async def test():
    pass
