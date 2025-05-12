from datetime import date, datetime
from uuid import UUID as uuid

from sqlalchemy import UUID, CheckConstraint, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oh_my_store.database.db import Base
from oh_my_store.enums import Gender


class AddressORM(Base):
    __tablename__ = "addresses"

    country: Mapped[str]
    city: Mapped[str]
    street: Mapped[str]


class ClientORM(Base):
    __tablename__ = "clients"

    client_name: Mapped[str] = mapped_column(String(100), nullable=False)
    client_surname: Mapped[str] = mapped_column(String(100), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[Gender] = mapped_column(nullable=False)
    registration_date: Mapped[date] = mapped_column(Date, default=datetime.now().date())
    address_id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id"),
    )

    address: Mapped["AddressORM"] = relationship(lazy="immediate")


class ProductORM(Base):
    __tablename__ = "products"

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

    category: Mapped["CategoryORM"] = relationship(
        back_populates="products",
        lazy="immediate",
    )
    supplier: Mapped["SupplierORM"] = relationship(
        back_populates="products",
        lazy="immediate",
    )
    image: Mapped["ImageORM"] = relationship(
        lazy="immediate",
    )

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_positive"),
        CheckConstraint("available_stock >= 0", name="check_available_stock_positive"),
    )


class CategoryORM(Base):
    __tablename__ = "categories"

    category_name: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[list["ProductORM"]] = relationship(back_populates="category")


class SupplierORM(Base):
    __tablename__ = "suppliers"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    address_id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id"),
    )

    address: Mapped["AddressORM"] = relationship(lazy="immediate")
    products: Mapped[list["ProductORM"]] = relationship(back_populates="supplier")


class ImageORM(Base):
    __tablename__ = "images"

    image_name: Mapped[bytes] = mapped_column(nullable=False)

    product: Mapped["ProductORM"] = relationship(back_populates="image")
