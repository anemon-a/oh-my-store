from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from oh_my_store.domain import Address, Client
from oh_my_store.database.orm.models import ClientORM
from oh_my_store.repositories import AbstractRepository
from oh_my_store.utils import to_dataclass, to_orm


class ClientSQLAlchemytRepository(AbstractRepository[Client]):

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_by_id(self, id: UUID) -> Client | None:
        client: ClientORM | None = await self._session.get(ClientORM, id)

        if client:
            client = to_dataclass(client, Client)

        return client

    async def get(self, first_name: str, last_name: str) -> Client | None:
        query = (
            select(ClientORM)
            .where(ClientORM.client_name == first_name)
            .where(ClientORM.client_surname == last_name)
        )
        client: ClientORM | None = await self._session.scalar(query)

        if client:
            client = to_dataclass(client, Client)

        return client

    async def list(self, limit: int, offset: int) -> list[Client]:
        clients = (
            await self._session.scalars(select(ClientORM).limit(limit).offset(offset))
        ).all()

        clients: list[Client] = [to_dataclass(client, Client) for client in clients]

        return clients

    async def add(self, client_data: Client) -> Client:
        client = to_orm(client_data, ClientORM)
        self._session.add(client)
        await self._session.flush()

        return to_dataclass(client, Client)

    async def delete(self, id: UUID) -> bool:
        client: ClientORM | None = await self._session.get(ClientORM, id)

        if not client:
            return False

        await self._session.delete(client)

        return True

    async def update(self, id: UUID, address: Address) -> Client | None:
        client: ClientORM | None = await self._session.get(ClientORM, id)

        if not client:
            return None

        client.address.country = address.country
        client.address.city = address.city
        client.address.street = address.street

        return to_dataclass(client, Client)
