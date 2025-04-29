from uuid import UUID
from dataclasses import dataclass
from oh_my_store.domain import Address


@dataclass
class Supplier:
    name: str
    address: Address
    phone_number: str
    id: UUID = None


    
