from uuid import UUID

from oh_my_store.entities import Address, Client
from oh_my_store.exceptions import ClientNotFoundError
from oh_my_store.services.unit_of_work import AbstractUnitOfWork


class ClientService:
    def __init__(self, unit_of_work: AbstractUnitOfWork) -> None:
        self._unit_of_work: AbstractUnitOfWork = unit_of_work

    async def get_by_name_and_surname(self, name: str, surname: str) -> Client | None:
        async with self._unit_of_work as uow:
            client: Client | None = await uow._clients.get(name=name, surname=surname)
            if not client:
                raise ClientNotFoundError(name=name, surname=surname)

            return client

    async def get_all(self, limit: int, offset: int) -> list[Client]:
        async with self._unit_of_work as uow:
            clients: list[Client] = await uow._clients.list(limit, offset)
            return clients

    async def create(self, client_data: Client) -> Client:
        async with self._unit_of_work as uow:
            client: Client = await uow._clients.add(client_data)
            return client

    async def delete_by_id(self, client_id: UUID) -> bool:
        async with self._unit_of_work as uow:
            deleted: bool = await uow._clients.delete(client_id)
            return deleted

    async def update_address_by_id(
        self, client_id: UUID, new_address: Address
    ) -> Client | None:
        async with self._unit_of_work as uow:
            client: Client | None = await uow._clients.update(
                client_id, address=new_address
            )
            if not client:
                raise ClientNotFoundError(client_id=client_id)
            return client
