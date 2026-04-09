from sqlmodel import Field, SQLModel, String
from decimal import Decimal
from pydantic import Field, field_validator
from datetime import datetime

# products table api models
class ProductPublic(SQLModel):
    id: int
    name: str
    current_price: Decimal 

class ProductCreate(SQLModel):
    name: str = Field(max_length=50)
    current_price: Decimal = Field(max_digits=10, decimal_places=3)

# countries table api models
class CountryPublic(SQLModel):
    id: int
    name: str

class CountryCreate(SQLModel):
    name: str = Field(max_length=50)

# customers table api models
class CustomerPublic(SQLModel):
    id: int
    username: str 
    email: str
    name: str
    country_id: int
    country_name: str

class CustomerCreate(SQLModel):
    name: str = Field(max_length=50)
    username: str = Field(max_length=50)
    email: str = Field(max_length=100)
    country_id: int

# status table api models
class StatusPublic(SQLModel):
    id: int
    name: str

class StatusCreate(SQLModel):
    name: str = Field(max_length=50)

# order items api models
class OrderItemPublic(SQLModel):
    id: int
    product_id: int
    order_id: int
    quantity: int
    price_per_unit_at_purchase: Decimal

class OrderItemCreate(SQLModel):
    quantity: int
    product_id: int

# orders table api models
class OrderPublic(SQLModel):
    id: int
    created_at: datetime
    status_last_updated_at: datetime
    current_status_id: int
    customer_id: int 
    tax_amount: Decimal
    discount_amount: Decimal
    shipping_costs_amount: Decimal

class OrderCreate(SQLModel):
    customer_id: int
    items: list[OrderItemCreate]  
    tax_amount: Decimal = Field(max_digits=10, decimal_places=3)
    discount_amount: Decimal = Field(max_digits=10, decimal_places=3)
    shipping_costs_amount: Decimal = Field(max_digits=10, decimal_places=3)

    # check if there are duplicated product IDs in the list of items purchased
    # throw error if they exist
    @field_validator('items', mode='after')  
    @classmethod
    def no_duplicate_product_id(cls, items: list):
       product_ids = [item.dict()['product_id'] for item in items]

       if len(product_ids) != len(set(product_ids)):
        raise ValueError("Unexpected behavior detected: duplicated product IDs in one order")

       return items

class OrderUpdate(SQLModel):
    current_status_id: int
    