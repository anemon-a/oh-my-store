from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from oh_my_store.utils import to_pydantic, to_dataclass
from oh_my_store.api.dependencies import get_unit_of_work
from oh_my_store.domain import Supplier, Address
from oh_my_store.schemas import SupplierResponse, SupplierCreate, AddressCreate
from oh_my_store.services import SupplierService
from oh_my_store.services.unit_of_work import AbstractUnitOfWork


router = APIRouter(prefix="/api/v1/supplier", tags=["suppliers"])


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier_by_id(
    supplier_id: UUID, uow: AbstractUnitOfWork = Depends(get_unit_of_work)
):
    supplier_service = SupplierService(uow)
    supplier: Supplier | None = await supplier_service.get_by_id(supplier_id)
    return to_pydantic(supplier, SupplierResponse)


@router.get("/", response_model=list[SupplierResponse])
async def get_all_suppliers(
    limit: int = 10,
    offset: int = 0,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
) -> list[SupplierResponse]:
    supplier_service = SupplierService(uow)
    suppliers: list[Supplier] = await supplier_service.get_all(limit, offset)

    return [to_pydantic(supplier, SupplierResponse) for supplier in suppliers]


@router.post("/", response_model=SupplierResponse)
async def create_supplier(
    supplier_data: SupplierCreate, uow: AbstractUnitOfWork = Depends(get_unit_of_work)
) -> SupplierResponse:
    supplier_service = SupplierService(uow)
    supplier: Supplier = await supplier_service.create(
        to_dataclass(supplier_data, Supplier)
    )
    return to_pydantic(supplier, SupplierResponse)


@router.patch("/{supplier_id}", response_model=SupplierResponse)
async def update_supplier_address_by_id(
    supplier_id: UUID,
    address_data: AddressCreate,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
):
    supplier_service = SupplierService(uow)
    supplier: Supplier | None = await supplier_service.update_address_by_id(
        supplier_id, to_dataclass(address_data, Address)
    )

    return to_pydantic(supplier, SupplierResponse)


@router.delete("/{supplier_id}")
async def delete_supplier_by_id(
    supplier_id: UUID,
    uow: AbstractUnitOfWork = Depends(get_unit_of_work),
):
    supplier_service = SupplierService(uow)
    deleted: bool = await supplier_service.delete_by_id(supplier_id)

    return deleted
