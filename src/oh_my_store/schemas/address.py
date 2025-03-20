from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    country: str = Field(min_length=1, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    street: str = Field(min_length=1, max_length=100)

    class Config:
        from_attributes = True


class AddressCreate(AddressBase):
    pass
