from oh_my_store.repository.client_repository_interface import IClientRepository
from oh_my_store.schemas.client import ClientCreate, ClientResponse


class ClientService:

    def __init__(self, client_repository: IClientRepository):
        self.client_repository = client_repository

    async def create_client(self, client_data: ClientCreate) -> ClientResponse:
        created_client = ClientResponse(
            **(await self.client_repository.add_client(client_data.model_dump()))
        )

        return created_client
