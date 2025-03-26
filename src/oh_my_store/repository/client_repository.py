from uuid import UUID
from typing import Sequence
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from oh_my_store.database.orm.models import ClientORM, AddressORM
from oh_my_store.schemas.address import AddressCreate
from oh_my_store.schemas.client import ClientCreate


class IClientRepository(ABC):
    @abstractmethod
    async def get_by_id(self, client_id: UUID) -> ClientORM | None:
        pass

    @abstractmethod
    async def get_by_name_and_surname(
        self, first_name: str, last_name: str
    ) -> ClientORM | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[ClientORM]:
        pass

    @abstractmethod
    async def create(self, client_data: ClientCreate) -> ClientORM:
        pass

    @abstractmethod
    async def delete_by_id(self, client_id: UUID) -> bool:
        pass

    @abstractmethod
    async def update_address_by_id(
        self, client_id: UUID, address: AddressCreate
    ) -> ClientORM | None:
        pass


class ClientRepository(IClientRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_by_id(self, id: UUID) -> ClientORM | None:
        client: ClientORM | None = await self.session.get(ClientORM, id)
        return client

    async def get_by_name_and_surname(
        self, first_name: str, last_name: str
    ) -> ClientORM | None:
        query = select(ClientORM).where(
            ClientORM.client_name == first_name
            and ClientORM.client_surname == last_name
        )
        client: ClientORM | None = await self.session.scalar(query)
        return client

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[ClientORM]:
        clients: Sequence[ClientORM] = (
            await self.session.scalars(select(ClientORM).limit(limit).offset(offset))
        ).all()

        return clients

    async def create(self, client_data: ClientCreate) -> ClientORM:
        address = AddressORM(**client_data.address.model_dump())
        # self.session.add(address)
        # await self.session.commit()
        # await self.session.refresh(address)

        client = ClientORM(**client_data.model_dump())
        client.address = address
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)

        return client

    async def delete_by_id(self, id: UUID) -> bool:
        client: ClientORM | None = await self.get_by_id(id)

        if not client:
            return False

        await self.session.delete(client)
        await self.session.commit()
        return True

    async def update_address_by_id(
        self, id: UUID, address: AddressCreate
    ) -> ClientORM | None:
        client: ClientORM | None = await self.get_by_id(id)

        if not client:
            return None

        client.address = AddressORM(**address.model_dump())
        await self.session.commit()
        await self.session.refresh(client)

        return client
