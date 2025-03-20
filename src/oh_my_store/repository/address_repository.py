from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from oh_my_store.db.models.models import Address as AddressORM
from oh_my_store.schemas.address import Address


class IAddressRepository(ABC):
    @abstractmethod
    async def create_address(address_data: Address) -> AddressORM:
        pass


class AddressRepository(IAddressRepository):

    @abstractmethod
    async def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create_address(self, address_data: Address) -> AddressORM:
        address = AddressORM(**address_data)
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)

        return address
