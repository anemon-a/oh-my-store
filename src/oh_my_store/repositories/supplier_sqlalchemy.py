from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from oh_my_store.domain import Supplier, Address
from oh_my_store.repositories import AbstractRepository
from oh_my_store.utils import to_dataclass, to_orm
from oh_my_store.database.orm.models import SupplierORM


class SupplierSQLAlchemyRepository(AbstractRepository[Supplier]):

    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def get_by_id(self, id: UUID) -> Supplier | None:
        supplier: SupplierORM | None = await self._session.get(SupplierORM, id)

        if supplier:
            supplier = to_dataclass(supplier, Supplier)

        return supplier

    async def get(self, **kwargs) -> Supplier | None:
        pass

    async def list(self, limit: int, offset: int) -> list[Supplier]:
        suppliers = (
            await self._session.scalars(select(SupplierORM).limit(limit).offset(offset))
        ).all()

        return [to_dataclass(supplier, Supplier) for supplier in suppliers]

    async def add(self, supplier_data: Supplier) -> Supplier:
        supplier_orm = to_orm(supplier_data, SupplierORM)

        self._session.add(supplier_orm)
        await self._session.flush()

        return to_dataclass(supplier_orm, Supplier)

    async def delete(self, id: UUID) -> bool:
        supplier: SupplierORM | None = await self._session.get(SupplierORM, id)

        if not supplier:
            return False

        await self._session.delete(supplier)

        return True

    async def update(self, id: UUID, address: Address) -> Supplier | None:
        supplier: SupplierORM | None = await self._session.get(SupplierORM, id)
        if not supplier:
            return None

        supplier.address.country = address.country
        supplier.address.city = address.city
        supplier.address.street = address.street

        return to_dataclass(supplier, Supplier)
