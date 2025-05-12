from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from oh_my_store.database.orm.models import SupplierORM
from oh_my_store.entities import Address, Supplier
from oh_my_store.repositories import AbstractRepository
from oh_my_store.utils import to_dataclass, to_orm


class SupplierSQLAlchemyRepository(AbstractRepository[Supplier]):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_by_id(self, id: UUID) -> Supplier | None:
        supplier_orm: SupplierORM | None = await self._session.get(SupplierORM, id)

        if supplier_orm:
            return to_dataclass(supplier_orm, Supplier)

        return None

    async def get(self, **kwargs) -> Supplier | None:
        pass

    async def list(self, limit: int, offset: int) -> list[Supplier]:
        supliers_orm = (
            await self._session.scalars(select(SupplierORM).limit(limit).offset(offset))
        ).all()

        return [to_dataclass(suplier_orm, Supplier) for suplier_orm in supliers_orm]

    async def add(self, supplier_data: Supplier) -> Supplier:
        supplier_orm = to_orm(supplier_data, SupplierORM)

        self._session.add(supplier_orm)
        await self._session.flush()

        return to_dataclass(supplier_orm, Supplier)

    async def delete(self, id: UUID) -> bool:
        supplier_orm: SupplierORM | None = await self._session.get(SupplierORM, id)

        if not supplier_orm:
            return False

        await self._session.delete(supplier_orm)

        return True

    async def update(self, id: UUID, **kwargs: Any) -> Supplier | None:
        supplier_orm: SupplierORM | None = await self._session.get(SupplierORM, id)
        if not supplier_orm:
            return None

        address: Address = kwargs["address"]

        supplier_orm.address.country = address.country
        supplier_orm.address.city = address.city
        supplier_orm.address.street = address.street

        return to_dataclass(supplier_orm, Supplier)
