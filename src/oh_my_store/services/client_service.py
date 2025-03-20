from uuid import UUID
from oh_my_store.repository.client_repository import IClientRepository
from oh_my_store.schemas.client import ClientCreate, ClientResponse
from oh_my_store.schemas.address import AddressCreate


class ClientService:

    def __init__(self, client_repository: IClientRepository):
        self.client_repository = client_repository

    async def get_client_by_name_and_surname(
        self, first_name: str, last_name: str
    ) -> ClientResponse | None:
        client = await self.client_repository.get_client_by_name_and_surname(
            first_name, last_name
        )
        if not client:
            return None
        return ClientResponse.model_validate(client)

    async def get_all_clients(
        self, limit: int = 10, offset: int = 0
    ) -> list[ClientResponse]:
        clients = await self.client_repository.get_all_clients(limit, offset)
        return [ClientResponse.model_validate(client) for client in clients]

    async def create_client(self, client_data: ClientCreate) -> ClientResponse:
        client = await self.client_repository.add_client(client_data)
        return ClientResponse.model_validate(client)

    async def delete_client_by_id(self, client_id: UUID) -> bool:
        deleted = await self.client_repository.delete_client_by_id(client_id)
        return deleted

    async def update_client_address_by_id(
        self, client_id: UUID, address_data: AddressCreate
    ) -> ClientResponse | None:

        client = await self.client_repository.update_client_address_by_id(
            client_id, address_data
        )
        if not client:
            return None

        return ClientResponse.model_validate(client)
