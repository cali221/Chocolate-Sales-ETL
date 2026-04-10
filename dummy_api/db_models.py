from sqlmodel import Field, SQLModel, String
from sqlalchemy import Column, TIMESTAMP, text
from datetime import datetime
from decimal import Decimal

class Product(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "products"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50), 
                      index=False, 
                      nullable=False, 
                      unique=True, 
                      max_length=50, 
                      min_length=1)
    current_price: Decimal = Field(nullable=False, max_digits=10, decimal_places=3, ge=0)

class Country(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "countries"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50), 
                      index=False, 
                      nullable=False, 
                      unique=True, 
                      max_length=50, 
                      min_length=2)

class Customer(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "customers"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50), index=False, nullable=False, max_length=50, min_length=1)
    username: str = Field(sa_type=String(50), index=False, nullable=False, unique=True, max_length=50, min_length=1)
    email: str = Field(sa_type=String(100), index=False, nullable=False, unique=True, max_length=100, min_length=2)
    country_id: int = Field(nullable=False, foreign_key="oltp_online_store.countries.id")

class Status(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "statuses"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50), index=False, nullable=False, unique=True, max_length=50, min_length=1)

class Order(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "orders"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    status_last_updated_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    current_status_id: int = Field(nullable=False, foreign_key="oltp_online_store.statuses.id")
    customer_id: int = Field(nullable=False, foreign_key="oltp_online_store.customers.id")
    tax_amount: Decimal = Field(nullable=False, max_digits=10, decimal_places=3, ge=0)
    discount_amount: Decimal = Field(nullable=False, max_digits=10, decimal_places=3, ge=0)
    shipping_costs_amount: Decimal = Field(nullable=False, max_digits=10, decimal_places=3, ge=0)

class StatusHistory(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "order_status_history"
    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(nullable=False, foreign_key="oltp_online_store.orders.id")
    status_id: int = Field(nullable=False, foreign_key="oltp_online_store.statuses.id")
    updated_at: datetime = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))

class OrderItem(SQLModel, table=True):
    __table_args__ = {"schema": "oltp_online_store"}
    __tablename__ = "order_items"
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(nullable=False, foreign_key="oltp_online_store.products.id")
    order_id: int = Field(nullable=False, foreign_key="oltp_online_store.orders.id")
    quantity: int = Field(nullable=False, ge=1)
    price_per_unit_at_purchase: Decimal = Field(nullable=False, max_digits=10, decimal_places=3, ge=0)
