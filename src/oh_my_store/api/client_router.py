from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from oh_my_store.api.mapper import Mapper
from oh_my_store.api.dependencies import get_uow
from oh_my_store.domain import Client, Address
from oh_my_store.services import ClientService
from oh_my_store.schemas import AddressCreate, ClientCreate, ClientResponse
from oh_my_store.services.unit_of_work import AbstractUnitOfWork

router = APIRouter(prefix="/api/v1/clients")


@router.get("/", response_model=list[ClientResponse])
async def get_all_clients(
    limit: int = 10,
    offset: int = 0,
    uow: AbstractUnitOfWork = (Depends(get_uow)),
) -> list[ClientResponse]:
    client_service = ClientService(uow)
    clients: list[Client] = await client_service.get_all(limit, offset)

    return [ClientResponse.model_validate(client) for client in clients]


@router.get("/by-name", response_model=ClientResponse)
async def get_client_by_name_and_surname(
    name: str,
    surname: str,
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> ClientResponse:
    client_service = ClientService(uow)
    client: Client | None = await client_service.get_by_name_and_surname(name, surname)

    if client is None:
        raise HTTPException(404, "Client not found")

    return ClientResponse.model_validate(client)


@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    uow: AbstractUnitOfWork = (Depends(get_uow)),
) -> ClientResponse:
    client_service = ClientService(uow)
    client: Client = await client_service.create(
        Mapper[Client, ClientCreate].from_pydantic_to_domain(client_data, Client)
    )

    return ClientResponse.model_validate(client)


@router.patch("/{client_id}", response_model=ClientResponse)
async def update_client_address_by_id(
    client_id: UUID,
    address: AddressCreate,
    uow: AbstractUnitOfWork = (Depends(get_uow)),
) -> ClientResponse:
    client_service = ClientService(uow)
    client: ClientResponse | None = await client_service.update_address_by_id(
        client_id,
        Mapper[Address, AddressCreate].from_pydantic_to_domain(address, Address),
    )

    if client is None:
        raise HTTPException(404, "Client not found")

    return ClientResponse.model_validate(client)


@router.delete("/{client_id}")
async def delete_client_by_id(
    client_id: UUID,
    uow: AbstractUnitOfWork = (Depends(get_uow)),
) -> bool:
    client_service = ClientService(uow)
    deleted: bool = await client_service.delete_by_id(client_id)
    return deleted
