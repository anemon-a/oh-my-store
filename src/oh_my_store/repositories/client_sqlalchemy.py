from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from oh_my_store.database.orm.models import ClientORM
from oh_my_store.entities import Address, Client
from oh_my_store.repositories import AbstractRepository
from oh_my_store.utils import to_dataclass, to_orm


class ClientSQLAlchemytRepository(AbstractRepository[Client]):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_by_id(self, id: UUID) -> Client | None:
        client_orm: ClientORM | None = await self._session.get(ClientORM, id)

        if client_orm:
            return to_dataclass(client_orm, Client)

        return None

    async def get(self, **kwargs: Any) -> Client | None:
        name: str = kwargs["name"]
        surname: str = kwargs["surname"]
        query = (
            select(ClientORM)
            .where(ClientORM.client_name == name)
            .where(ClientORM.client_surname == surname)
        )
        client_orm: ClientORM | None = await self._session.scalar(query)

        if client_orm:
            return to_dataclass(client_orm, Client)

        return None

    async def list(self, limit: int, offset: int) -> list[Client]:
        clients_orm = (
            await self._session.scalars(select(ClientORM).limit(limit).offset(offset))
        ).all()

        return [to_dataclass(client_orm, Client) for client_orm in clients_orm]

    async def add(self, client_data: Client) -> Client:
        client_orm: ClientORM = to_orm(client_data, ClientORM)
        self._session.add(client_orm)
        await self._session.flush()

        return to_dataclass(client_orm, Client)

    async def delete(self, id: UUID) -> bool:
        client_orm: ClientORM | None = await self._session.get(ClientORM, id)

        if not client_orm:
            return False

        await self._session.delete(client_orm)

        return True

    async def update(self, id: UUID, **kwargs: Any) -> Client | None:
        client_orm: ClientORM | None = await self._session.get(ClientORM, id)

        if not client_orm:
            return None

        address: Address = kwargs["address"]

        client_orm.address.country = address.country
        client_orm.address.city = address.city
        client_orm.address.street = address.street

        return to_dataclass(client_orm, Client)
