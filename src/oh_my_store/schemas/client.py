from uuid import UUID
from datetime import date
from pydantic import BaseModel, Field, field_validator
from oh_my_store.schemas.address import AddressCreate
from oh_my_store.enums import Gender


class ClientBase(BaseModel):
    client_name: str = Field(min_length=1, max_length=100)
    client_surname: str = Field(min_length=1, max_length=100)
    birthday: date
    gender: Gender
    address: AddressCreate

    @field_validator("birthday")
    @classmethod
    def validate_birthday(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("Дата рождения не может быть в будущем.")
        return value


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: UUID
    registration_date: date

    class Config:
        from_attributes = True
