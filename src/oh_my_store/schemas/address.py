from uuid import UUID
from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    country: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    street: str = Field(min_length=1, max_length=100)


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id: UUID

    class Config:
        from_attributes = True
