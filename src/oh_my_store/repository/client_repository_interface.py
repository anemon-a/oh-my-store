from uuid import UUID
from abc import ABC, abstractmethod
from oh_my_store.db.models.models import Client as ClientORM
from oh_my_store.schemas.client import ClientCreate


class IClientRepository(ABC):
    @abstractmethod
    async def get_client_by_id(self, client_id: UUID) -> ClientORM | None:
        pass

    @abstractmethod
    async def get_client_by_name_and_surname(
        self, name: str, surname: str
    ) -> ClientORM | None:
        pass

    @abstractmethod
    async def get_all_clients(
        self, limit: int = 10, offset: int = 0
    ) -> list[ClientORM] | None:
        pass

    @abstractmethod
    async def add_client(self, client_data: ClientCreate) -> ClientORM:
        pass

    @abstractmethod
    async def delete_client_by_id(self, client_id: UUID) -> bool:
        pass

    @abstractmethod
    async def update_client_address_by_id(self, client_id: UUID) -> ClientORM:
        pass
