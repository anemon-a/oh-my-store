from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from oh_my_store.schemas.address import AddressCreate, AddressResponse


class SupplierBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone_number: str = Field()


class SupplierCreate(SupplierBase):
    address: AddressCreate


class SupplierResponse(SupplierBase):
    id: UUID
    address: AddressResponse

    class Config:
        from_attributes = True
