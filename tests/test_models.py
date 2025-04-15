import pytest
from datetime import date
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from oh_my_store.database.orm.models import Base
from oh_my_store.enums import Gender
from oh_my_store.domain import Client, Address
from oh_my_store.repositories.client_sqlalchemy import ClientSQLAlchemytRepository


@pytest.fixture(autouse=True)
async def session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(bind=engine)
    session: AsyncSession = async_session()
    yield session
    await session.close()


@pytest.fixture
async def addresses() -> list[Address]:
    addresses = [
        Address(country="Russia", city="Moscow", street="Kirova"),
        Address(country="Italy", city="Rome", street="Vinca"),
        Address(country="Japan", city="Tokyo", street="Izuka"),
    ]

    return addresses


@pytest.fixture
async def clients(addresses: list[Address]) -> list[Client]:
    clients: list[Client] = [
        Client(
            client_name="Aboba",
            client_surname="Abiba",
            birthday=date(2000, 12, 26),
            gender=Gender.FEMALE,
            address=addresses[0],
        ),
        Client(
            client_name="Dimka",
            client_surname="Lolkin",
            birthday=date(2002, 2, 2),
            gender=Gender.MALE,
            address=addresses[1],
        ),
    ]

    return clients


async def test_client_sqlalchemy_repository_add(
    clients: list[Client], session: AsyncSession
):
    repository = ClientSQLAlchemytRepository(session)
    client: Client = await repository.add(client_data=clients[0])
    assert client == await repository.get_by_id(client.id)
