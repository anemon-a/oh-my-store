from dataclasses import dataclass
from uuid import UUID

from oh_my_store.entities import Address


@dataclass
class Supplier:
    name: str
    address: Address
    phone_number: str
    id: UUID | None = None
