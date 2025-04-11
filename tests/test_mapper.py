import pytest
from uuid import UUID
from datetime import date
from pydantic import ValidationError
from oh_my_store.enums import Gender
from oh_my_store.utils import to_dataclass, to_orm, to_pydantic
from oh_my_store.domain import Address, Client
from oh_my_store.schemas import (
    ClientCreate,
    AddressCreate,
    ClientResponse,
    AddressResponse,
)
from oh_my_store.database.orm.models import ClientORM, AddressORM


@pytest.fixture
async def clients_domain() -> list[Client]:
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


@pytest.fixture
async def clients_orm() -> list[ClientORM]:
    clients: list[ClientORM] = [
        ClientORM(
            id=UUID("fa1bf33c-6d20-4099-9889-ff8de6df2c9d"),
            client_name="Aboba",
            client_surname="Abiba",
            birthday=date(2000, 12, 26),
            gender=Gender.FEMALE,
            address=AddressORM(
                id=UUID("a89e87fd-eaff-4e50-9472-9ac543e8ae08"),
                country="Russia",
                city="Moscow",
                street="Kirova",
            ),
            registration_date=date(2025, 1, 12),
        ),
        ClientORM(
            client_name="Dimka",
            client_surname="Lolkin",
            birthday=date(2002, 2, 2),
            gender=Gender.MALE,
            address=AddressORM(country="Italy", city="Rome", street="Vinca"),
        ),
    ]

    return clients


@pytest.fixture
async def clients_pydantic() -> tuple[ClientResponse, ClientCreate]:
    clients: tuple[ClientResponse, ClientCreate] = (
        ClientResponse(
            id=UUID("fa1bf33c-6d20-4099-9889-ff8de6df2c9d"),
            client_name="Aboba",
            client_surname="Abiba",
            birthday=date(2000, 12, 26),
            gender=Gender.FEMALE,
            address=AddressResponse(
                id=UUID("a89e87fd-eaff-4e50-9472-9ac543e8ae08"),
                country="Russia",
                city="Moscow",
                street="Kirova",
            ),
            registration_date=date(2025, 1, 12),
        ),
        ClientCreate(
            client_name="Dimka",
            client_surname="Lolkin",
            birthday=date(2002, 2, 2),
            gender=Gender.MALE,
            address=AddressCreate(country="Italy", city="Rome", street="Vinca"),
        ),
    )

    return clients


@pytest.mark.parametrize("id", [0, 1])
def test_mapper_orm_to_dataclass(
    clients_orm: list[ClientORM], clients_domain: list[Client], id: int
):
    assert clients_domain[id] == to_dataclass(clients_orm[id], Client)


@pytest.mark.parametrize("id", [0, 1])
def test_mapper_pydantic_to_dataclass(
    clients_pydantic: tuple[ClientResponse, ClientCreate],
    clients_domain: list[Client],
    id: int,
):
    print(clients_domain[id])
    assert clients_domain[id] == to_dataclass(clients_pydantic[id], Client)


@pytest.mark.parametrize("id", [0, 1])
def test_mapper_dataclass_to_orm(
    clients_domain: list[Client], clients_orm: list[ClientORM], id: int
):
    assert clients_orm[id] == to_orm(clients_domain[id], ClientORM)


@pytest.mark.parametrize("id", [0, 1])
def test_mapper_pydantic_to_orm(
    clients_pydantic: list[ClientCreate], clients_orm: list[ClientORM], id: int
):
    assert clients_orm[id] == to_orm(clients_pydantic[id], ClientORM)


@pytest.mark.parametrize("id", [0, 1])
def test_mapper_dataclass_to_pydantic(
    clients_domain: list[Client],
    clients_pydantic: tuple[ClientResponse, ClientCreate],
    id: int,
):
    if id == 0:
        assert clients_pydantic[id] == to_pydantic(clients_domain[id], ClientResponse)
    else:
        with pytest.raises(ValidationError):
            to_pydantic(clients_domain[id], ClientResponse)


@pytest.mark.parametrize("id", [0, 1])
def test_mapper_orm_to_pydantic(
    clients_orm: list[ClientORM],
    clients_pydantic: tuple[ClientResponse, ClientCreate],
    id: int,
):
    if id == 0:
        assert clients_pydantic[id] == to_pydantic(clients_orm[id], ClientResponse)
    else:
        with pytest.raises(ValidationError):
            to_pydantic(clients_orm[id], ClientResponse)
