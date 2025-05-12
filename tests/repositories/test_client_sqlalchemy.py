from dataclasses import fields
from datetime import date
from uuid import UUID, uuid4

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from oh_my_store.database.orm.models import Base
from oh_my_store.entities import Address, Client
from oh_my_store.enums import Gender
from oh_my_store.repositories.client_sqlalchemy import ClientSQLAlchemytRepository


@pytest.fixture
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(autouse=True)
async def session(engine: AsyncSession):
    async_session = async_sessionmaker(bind=engine)
    session: AsyncSession = async_session()
    yield session
    await session.close()


@pytest.fixture
async def clients() -> list[Client]:
    clients: list[Client] = [
        Client(
            id=UUID("fa1bf33c-6d20-4099-9889-ff8de6df2c9d"),
            client_name="Aboba",
            client_surname="Abiba",
            birthday=date(2000, 12, 26),
            gender=Gender.FEMALE,
            address=Address(
                id=UUID("a89e87fd-eaff-4e50-9472-9ac543e8ae08"),
                country="Russia",
                city="Moscow",
                street="Kirova",
            ),
            registration_date=date(2025, 1, 12),
        ),
        Client(
            client_name="Dimka",
            client_surname="Lolkin",
            birthday=date(2002, 2, 2),
            gender=Gender.MALE,
            address=Address(country="Italy", city="Rome", street="Vinca"),
        ),
    ]
    return clients


async def test_add_and_get_by_id(session: AsyncSession, clients: list[Client]):
    repository = ClientSQLAlchemytRepository(session)
    client_to_add = clients[0]

    added_client = await repository.add(client_to_add)
    await session.commit()

    retrieved_client = await repository.get_by_id(added_client.id)

    assert retrieved_client is not None
    for field in fields(client_to_add):
        assert getattr(retrieved_client, field.name) == getattr(
            client_to_add, field.name
        )


async def test_get_by_id_not_found(session: AsyncSession):
    repository = ClientSQLAlchemytRepository(session)
    non_existent_id = uuid4()

    result = await repository.get_by_id(non_existent_id)

    assert result is None


async def test_get_by_name_and_surname(session: AsyncSession, clients: list[Client]):
    repository = ClientSQLAlchemytRepository(session)
    client_to_add = clients[0]
    await repository.add(client_to_add)
    await session.commit()

    result = await repository.get(
        name=client_to_add.client_name, surname=client_to_add.client_surname
    )

    assert result is not None
    assert result.client_name == client_to_add.client_name
    assert result.client_surname == client_to_add.client_surname


async def test_list(session: AsyncSession, clients: list[Client]):
    repository = ClientSQLAlchemytRepository(session)
    for client in clients:
        await repository.add(client)

    await session.commit()

    result = await repository.list(limit=10, offset=0)

    assert len(result) == len(clients)
    assert all(
        any(
            r.client_name == c.client_name and r.client_surname == c.client_surname
            for c in clients
        )
        for r in result
    )


async def test_delete(session: AsyncSession, clients: list[Client]):
    repository = ClientSQLAlchemytRepository(session)
    client_to_add = clients[0]
    added_client = await repository.add(client_to_add)
    await session.commit()

    delete_result = await repository.delete(added_client.id)
    await session.commit()
    retrieved_client = await repository.get_by_id(added_client.id)

    assert delete_result is True
    assert retrieved_client is None


async def test_delete_not_found(session: AsyncSession):
    repository = ClientSQLAlchemytRepository(session)
    non_existent_id = uuid4()

    result = await repository.delete(non_existent_id)

    assert result is False


async def test_update(session: AsyncSession, clients: list[Client]):
    repository = ClientSQLAlchemytRepository(session)
    client_to_add = clients[0]
    added_client = await repository.add(client_to_add)
    await session.commit()
    new_address = Address(country="USA", city="New York", street="Broadway")

    updated_client = await repository.update(added_client.id, address=new_address)
    retrieved_client = await repository.get_by_id(added_client.id)

    assert updated_client is not None
    assert retrieved_client is not None
    assert retrieved_client.address.country == new_address.country
    assert retrieved_client.address.city == new_address.city
    assert retrieved_client.address.street == new_address.street


async def test_update_not_found(session: AsyncSession):
    repository = ClientSQLAlchemytRepository(session)
    non_existent_id = uuid4()
    new_address = Address(country="USA", city="New York", street="Broadway")
    await session.commit()

    result = await repository.update(non_existent_id, address=new_address)

    assert result is None
