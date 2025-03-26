from abc import ABC, abstractmethod
from uuid import UUID


class AbstractRepository[T](ABC):
    @abstractmethod
    async def get_by_id(self, id: UUID) -> T | None:
        pass

    @abstractmethod
    async def get(self, **kwargs) -> T | None:
        pass

    @abstractmethod
    async def list(self, limit: int, offset: int) -> list[T]:
        pass

    @abstractmethod
    async def add(self, data: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    async def update(self, id: UUID, **kwargs) -> T | None:
        pass
