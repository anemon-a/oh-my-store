from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from oh_my_store.db.models.models import Client as ClientORM, Address as AddressORM
from oh_my_store.repository.client_repository_interface import IClientRepository
from oh_my_store.repository.address_repository import (
    IAddressRepository,
    AddressRepository,
)
from oh_my_store.schemas.client import ClientCreate


class ClientRepository(IClientRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_client_by_id(self, id: UUID) -> ClientORM | None:
        client: ClientORM | None = await self.session.get(ClientORM, id)
        return client

    async def get_client_by_name_and_surname(
        self, name: str, surname: str
    ) -> ClientORM | None:
        query = select(ClientORM).where(
            ClientORM.client_name == name and ClientORM.client_surname == surname
        )
        client: ClientORM | None = await self.session.scalar(query)
        return client

    async def get_all_clients(
        self, limit: int = 10, offset: int = 0
    ) -> list[ClientORM]:
        clients: list[ClientORM] = [
            (
                await self.session.scalars(
                    select(ClientORM).limit(limit).offset(offset)
                )
            ).all()
        ]
        return clients

    async def add_client(self, client_data: dict) -> ClientORM:

        address = AddressORM(**client_data["address"])
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)

        client = ClientORM(**client_data)
        client.address_id = address.id
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)

        return client

    async def delete_client_by_id(self, id: UUID) -> bool:
        client: ClientORM | None = await self.get_client_by_id(id)

        if not client:
            return False

        await self.session.delete(client)
        await self.session.commit()
        return True

    async def update_client_address_by_id(self, id: UUID, address) -> ClientORM | None:
        client: ClientORM | None = await self.get_client_by_id(id)

        if not client:
            return None

        client.address = AddressORM(**address)
        await self.session.commit()
        await self.session.refresh(client)

        return client
