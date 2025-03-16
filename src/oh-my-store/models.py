from typing import Annotated
from uuid import UUID as uuid, uuid4
from sqlalchemy import CheckConstraint, Constraint, Date, Enum, UUID, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import date, datetime


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Gender(Enum):
    male = 1
    female = 2


uuid_pk = Annotated[
    uuid, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
]
str100 = Annotated[str, mapped_column(String(100))]


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid_pk]
    client_name: Mapped[str100]
    client_surname: Mapped[str100]
    birthday: Mapped[date]
    gender: Mapped[Gender] = mapped_column(Gender)
    registration_date: Mapped[date] = mapped_column(Date, default=datetime.now().date())
    address_id: Mapped[uuid] = mapped_column(ForeignKey("addresses.id"))


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid_pk]
    name: Mapped[str100]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    price: Mapped[float] = mapped_column(default=0)
    available_stock: Mapped[int] = mapped_column(default=0)
    last_update_date: Mapped[date]
    supplier_id: Mapped[uuid] = mapped_column(ForeignKey("suppliers.id"))
    image_id: Mapped[uuid] = mapped_column(ForeignKey("images.id"))

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_positive"),
        CheckConstraint("available_stock >= 0", name="check_available_stock_positive"),
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid_pk]
    category_name: Mapped[str100]


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[uuid_pk]
    name: Mapped[str100]
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    phone_number: Mapped[str] = mapped_column(unique=True)


class Image(Base):
    __tablename__ = "images"

    id: Mapped[uuid_pk]
    image: Mapped[bytearray]


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[uuid_pk]
    country: Mapped[str100]
    city: Mapped[str100]
    street: Mapped[str100]
