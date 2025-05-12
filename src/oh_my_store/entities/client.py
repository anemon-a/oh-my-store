from dataclasses import dataclass
from datetime import date
from uuid import UUID

from oh_my_store.entities import Address
from oh_my_store.enums import Gender


@dataclass
class Client:
    client_name: str
    client_surname: str
    birthday: date
    gender: Gender
    address: Address
    id: UUID | None = None
    registration_date: date | None = None
