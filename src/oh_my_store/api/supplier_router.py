from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends

from oh_my_store.api.dependencies import get_uow
from oh_my_store.schemas import SupplierResponse, SupplierCreate, AddressCreate
from oh_my_store.domain import Supplier, Address
from oh_my_store.services.unit_of_work import AbstractUnitOfWork


router = APIRouter(prefix="/api/v1/supplier")


@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier_by_id(
    supplier_id: UUID, uow: AbstractUnitOfWork = Depends(get_uow)
):
    pass
