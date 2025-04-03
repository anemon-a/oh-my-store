from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from oh_my_store.domain import Supplier, Address
from oh_my_store.repositories import AbstractRepository
from oh_my_store.repositories.mapper import Mapper
from oh_my_store.database.orm.models import AddressORM, SupplierORM


class SQLAlchemySupplierRepository(AbstractRepository[Supplier]):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self._supplier_mapper = Mapper[Supplier, SupplierORM]()

    async def get_by_id(self, id: UUID) -> Supplier | None:
        supplier: SupplierORM | None = await self._session.get(SupplierORM, id)
        return self._supplier_mapper.from_orm_to_domain(supplier, Supplier)

    async def get(self, **kwargs) -> Supplier | None:
        pass

    async def list(self, limit: int, offset: int) -> list[Supplier]:
        suppliers = (
            await self._session.scalars(select(SupplierORM).limit(limit).offset(offset))
        ).all()

        return [
            self._supplier_mapper.from_orm_to_domain(supplier, Supplier)
            for supplier in suppliers
        ]

    async def add(self, supplier_data: Supplier) -> Supplier:
        supplier_orm = self._supplier_mapper.from_domain_to_orm(
            supplier_data, SupplierORM
        )

        self._session.add(supplier_orm)
        self._session.flush()

        return self._supplier_mapper.from_orm_to_domain(supplier_orm, Supplier)

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

        address_mapper = Mapper[Address, AddressORM]()

        supplier.address = address_mapper.from_domain_to_orm(address, AddressORM)
        return self._supplier_mapper.from_orm_to_domain(supplier, Supplier)
