from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from oh_my_store.services.client_service import ClientService
from oh_my_store.api.dependencies import get_client_service
from oh_my_store.schemas.address import AddressCreate
from oh_my_store.schemas.client import ClientCreate, ClientResponse

router = APIRouter(prefix="/api/v1/clients")


@router.get("/", response_model=list[ClientResponse])
async def get_all_clients(
    limit: int = 10,
    offset: int = 0,
    client_service: ClientService = Depends(get_client_service),
) -> list[ClientResponse]:
    client: list[ClientResponse] = await client_service.get_all_clients(limit, offset)

    return client


@router.get("/by-name", response_model=ClientResponse)
async def get_client_by_first_name_and_last_name(
    first_name: str,
    last_name: str,
    client_service: ClientService = Depends(get_client_service),
) -> ClientResponse:
    client: ClientResponse | None = await client_service.get_client_by_name_and_surname(
        first_name, last_name
    )

    if client is None:
        raise HTTPException(404, "Client not found")

    return client


@router.post("/", response_model=ClientResponse)
async def create_client(
    client: ClientCreate, client_service: ClientService = Depends(get_client_service)
) -> ClientResponse:
    new_client: ClientResponse = await client_service.create_client(client)
    return new_client


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client_address_by_id(
    client_id: UUID,
    address: AddressCreate,
    client_service: ClientService = Depends(get_client_service),
) -> ClientResponse:
    client: ClientResponse | None = await client_service.update_client_address_by_id(
        client_id, address
    )

    if client is None:
        raise HTTPException(404, "Client not found")

    return client


@router.delete("/{client_id}")
async def delete_client_by_id(
    client_id: UUID,
    client_service: ClientService = Depends(get_client_service),
) -> bool:
    deleted: ClientResponse | None = await client_service.delete_client_by_id(client_id)
    return deleted
