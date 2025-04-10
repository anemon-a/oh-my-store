from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from oh_my_store.schemas.address import AddressCreate, AddressResponse


class SupplierBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone_number: str = Field()


class SupplierCreate(SupplierBase):
    address: AddressCreate


class SupplierResponse(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    address: AddressResponse
