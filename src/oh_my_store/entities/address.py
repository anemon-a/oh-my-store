from dataclasses import dataclass
from uuid import UUID


@dataclass
class Address:
    country: str
    city: str
    street: str
    id: UUID | None = None
