from fastapi import APIRouter, Depends
from oh_my_store.services.client_service import ClientService
from oh_my_store.routers.dependencies import get_client_service
from oh_my_store.schemas.client import ClientCreate, ClientResponse

router = APIRouter()


@router.post("/clients", response_model=ClientResponse)
async def create_client(
    client: ClientCreate, client_service: ClientService = Depends(get_client_service)
) -> ClientResponse:
    return await client_service.create_client(client)
