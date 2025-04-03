from uuid import UUID
from oh_my_store.services.unit_of_work import AbstractUnitOfWork
from oh_my_store.domain import Supplier, Address


class SupplierService:

    def __init__(self, unit_of_work: AbstractUnitOfWork):
        self._uow: AbstractUnitOfWork = unit_of_work

    async def get_supplier_by_id(self, supplier_id: UUID) -> Supplier | None:
        async with self._uow as uow:
            supplier: Supplier | None = await uow._suppliers.get_by_id(supplier_id)
            return supplier

    async def get_all(self, limit: int, offset: int) -> list[Supplier]:
        async with self._uow as uow:
            suppliers: list[Supplier] = await uow._suppliers.list(limit, offset)
            return suppliers

    async def create(self, supplier_data: Supplier) -> Supplier:
        async with self._uow as uow:
            supplier: Supplier = await uow._suppliers.add(supplier_data)
            return supplier

    async def delete_by_id(self, supplier_id: UUID) -> bool:
        async with self._uow as uow:
            deleted: bool = await uow._suppliers.delete(supplier_id)
            return deleted

    async def update_address_by_id(
        self, supplier_id: UUID, new_address: Address
    ) -> Supplier | None:
        async with self._uow as uow:
            supplier: Supplier | None = await uow._suppliers.update(
                supplier_id, new_address
            )
            return supplier
