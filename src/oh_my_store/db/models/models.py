from enum import Enum
from typing import Annotated
from uuid import UUID as uuid, uuid4
from sqlalchemy import CheckConstraint, UUID, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import date, datetime


class Gender(Enum):
    male = 1
    female = 2


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    country: Mapped[str]
    city: Mapped[str]
    street: Mapped[str]


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    client_name: Mapped[str] = mapped_column(String(100), nullable=False)
    client_surname: Mapped[str] = mapped_column(String(100), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[Gender] = mapped_column(nullable=False)
    registration_date: Mapped[date] = mapped_column(Date, default=datetime.now().date())
    address_id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id"),
    )

    address: Mapped["Address"] = relationship(lazy="immediate")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    available_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_update_date: Mapped[date] = mapped_column(Date)
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id"),
    )
    supplier_id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("suppliers.id"),
    )
    image_id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("images.id"),
    )

    category: Mapped["Category"] = relationship(
        back_populates="products",
        lazy="immediate",
    )
    supplier: Mapped["Supplier"] = relationship(
        back_populates="products",
        lazy="immediate",
    )
    image: Mapped["Image"] = relationship(
        back_populates="product",
        lazy="immediate",
    )

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_positive"),
        CheckConstraint("available_stock >= 0", name="check_available_stock_positive"),
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    address_id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id"),
    )

    address: Mapped["Address"] = relationship(lazy="immediate")
    products: Mapped[list["Product"]] = relationship(back_populates="supplier")


class Image(Base):
    __tablename__ = "images"

    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    image: Mapped[bytes] = mapped_column(nullable=False)

    product: Mapped["Image"] = relationship(back_populates="image")
