from uuid import UUID
from oh_my_store.entities.client import Client
from oh_my_store.repository.client_repository import IClientRepository
from oh_my_store.schemas.client import ClientCreate, ClientResponse
from oh_my_store.schemas.address import AddressCreate


class ClientService:

    def __init__(self, client_repository: IClientRepository):
        self.client_repository = client_repository

    async def get_client_by_name_and_surname(
        self, first_name: str, last_name: str
    ) -> ClientResponse | None:
        client: Client | None = await self.client_repository.get_by_name_and_surname(
            first_name, last_name
        )
        if not client:
            return None
        return ClientResponse.model_validate(client)

    async def get_all_clients(
        self, limit: int = 10, offset: int = 0
    ) -> list[ClientResponse]:
        clients: list[Client] = await self.client_repository.get_all(limit, offset)
        return [ClientResponse.model_validate(client) for client in clients]

    async def create_client(self, client_data: ClientCreate) -> ClientResponse:
        client = Client(client_data.dict)
        client: Client = await self.client_repository.create(client_data)
        return ClientResponse.model_validate(client)

    async def delete_client_by_id(self, client_id: UUID) -> bool:
        deleted = await self.client_repository.delete_by_id(client_id)
        return deleted

    async def update_client_address_by_id(
        self, client_id: UUID, address_data: AddressCreate
    ) -> ClientResponse | None:

        client: Client | None = await self.client_repository.update_address_by_id(
            client_id, address_data
        )
        if not client:
            return None

        return ClientResponse.model_validate(client)
