from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from oh_my_store.schemas.address import AddressCreate, AddressResponse


class SupplierBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone_number: PhoneNumber


class SupplierCreate(SupplierBase):
    address: AddressCreate


class SupplierResponse(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    address: AddressResponse
