from uuid import UUID
from dataclasses import dataclass
from oh_my_store.domain import Address


@dataclass
class Supplier:
    id: UUID
    name: str
    address: Address
    phone_number: str
