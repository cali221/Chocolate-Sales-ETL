from sqlmodel import Field, SQLModel, String
from sqlalchemy import Column, TIMESTAMP, text
from datetime import datetime
from decimal import Decimal

class DimensionsBase(SQLModel):
    name: str = Field(sa_type=String(100), index=False, nullable=False)

class Product(DimensionsBase, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "products"
    id: int | None = Field(default=None, primary_key=True)
    current_price: Decimal = Field(nullable=False, max_digits=10, decimal_places=3)

class Country(DimensionsBase, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "countries"
    id: int | None = Field(default=None, primary_key=True)

class Customer(DimensionsBase, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "customers"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_type=String(50), index=False, nullable=False)
    email: str = Field(sa_type=String(100), index=False, nullable=False)
    country_id: int = Field(nullable=False, foreign_key="oltp_online_store.countries.id")

class Status(DimensionsBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "status"

class Order(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "orders"
    id: int | None = Field(default=None, primary_key=True)
    total_amount: Decimal = Field(nullable=False, max_digits=15, decimal_places=3)
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    last_updated_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    current_status: int = Field(nullable=False, foreign_key="oltp_online_store.status.id")
    customer_id: int = Field(nullable=False, foreign_key="oltp_online_store.customers.id")

class StatusHistory(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "order_status_history"
    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(nullable=False, foreign_key="oltp_online_store.orders.id")
    status_id: int = Field(nullable=False, foreign_key="oltp_online_store.status.id")
    updated_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))

class OrderProduct(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "order_item"
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(nullable=False, foreign_key="oltp_online_store.products.id")
    order_id: int = Field(nullable=False, foreign_key="oltp_online_store.orders.id")
    quantity: int = Field(nullable=False)
    price_at_purchase: Decimal = Field(nullable=False, max_digits=15, decimal_places=3)
