from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from oh_my_store.domain import Client, Supplier
from oh_my_store.repositories import (
    AbstractRepository,
    ClientSQLAlchemytRepository,
    SupplierSQLAlchemyRepository,
)


class AbstractUnitOfWork(ABC):
    _clients: AbstractRepository[Client]
    _suppliers: AbstractRepository[Supplier]

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            await self.commit()
            return

        self.rollback()
        raise exc_value from tb

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class SQLAlchemyUnitOFWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self._session_factory()
        self._clients = ClientSQLAlchemytRepository(self.session)
        self._suppliers = SupplierSQLAlchemyRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
