from uuid import UUID
from sqlalchemy.exc import IntegrityError
from oh_my_store.domain import Supplier, Address
from oh_my_store.services.unit_of_work import AbstractUnitOfWork
from oh_my_store.exceptions import DuplicatePhoneNumberError, SupplierNotFoundError


class SupplierService:

    def __init__(self, unit_of_work: AbstractUnitOfWork):
        self._unit_of_work: AbstractUnitOfWork = unit_of_work

    async def get_by_id(self, supplier_id: UUID) -> Supplier | None:
        async with self._unit_of_work as uow:
            supplier: Supplier | None = await uow._suppliers.get_by_id(supplier_id)
            if not supplier:
                raise SupplierNotFoundError(supplier_id)

            return supplier

    async def get_all(self, limit: int, offset: int) -> list[Supplier]:
        async with self._unit_of_work as uow:
            suppliers: list[Supplier] = await uow._suppliers.list(limit, offset)
            return suppliers

    async def create(self, supplier_data: Supplier) -> Supplier:
        try:
            async with self._unit_of_work as uow:
                supplier: Supplier = await uow._suppliers.add(supplier_data)
                return supplier

        except IntegrityError as e:
            raise DuplicatePhoneNumberError(supplier_data.phone_number)

    async def delete_by_id(self, supplier_id: UUID) -> bool:
        async with self._unit_of_work as uow:
            deleted: bool = await uow._suppliers.delete(supplier_id)

            return deleted

    async def update_address_by_id(
        self, supplier_id: UUID, new_address: Address
    ) -> Supplier | None:
        async with self._unit_of_work as uow:
            supplier: Supplier | None = await uow._suppliers.update(
                supplier_id, new_address
            )
            if not supplier:
                raise SupplierNotFoundError(supplier_id)

            return supplier
