from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class AddressBase(BaseModel):
    country: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    street: str = Field(min_length=1, max_length=100)


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
