from uuid import UUID
from oh_my_store.domain import Address, Client
from oh_my_store.services.unit_of_work import AbstractUnitOfWork


class ClientService:

    def __init__(self, unit_of_work: AbstractUnitOfWork):
        self._uow = unit_of_work

    async def get_by_name_and_surname(self, name: str, surname: str) -> Client | None:
        async with self._uow as uow:
            client: Client | None = await uow._clients.get(name, surname)
            if not client:
                return None
            return client

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[Client]:
        async with self._uow as uow:
            clients: list[Client] = await uow._clients.list(limit, offset)
            return clients

    async def create(self, client_data: Client) -> Client:
        async with self._uow as uow:
            client: Client = await uow._clients.add(client_data)
            await uow.commit()
            return client

    async def delete_by_id(self, client_id: UUID) -> bool:
        async with self._uow as uow:
            deleted: bool = await uow._clients.delete(client_id)
            await uow.commit()
            return deleted

    async def update_address_by_id(
        self, client_id: UUID, address_data: Address
    ) -> Client | None:
        async with self._uow as uow:
            client: Client | None = await uow._clients.update(client_id, address_data)
            await uow.commit()
            if not client:
                return None

            return client
