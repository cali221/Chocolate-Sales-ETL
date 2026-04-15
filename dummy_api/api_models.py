from sqlmodel import Field, SQLModel
from decimal import Decimal
from pydantic import Field, field_validator, model_validator, PlainSerializer
from datetime import datetime
from typing_extensions import Annotated
from shared.oltp_db_models import ProductChannels 
from typing import Optional
from typing_extensions import Self
                        
# start of code I did not write myself
# copied from (as of April 9th 2026): https://github.com/pydantic/pydantic/issues/7457#issuecomment-2994018396
# author: samuelcolvin (username on GitHub)
# date of source's publication: Jun 22, 2025
FloatDecimal = Annotated[
    Decimal,
    PlainSerializer(float, return_type=float, when_used='json')
]
# end of code I did not write myself

# products table api models
class ProductPublic(SQLModel):
    id: int = Field(nullable=False)
    name: str = Field(min_length=1, nullable=False, max_length=50)
    current_price_online: Optional[FloatDecimal] = Field(max_digits=10, decimal_places=3, ge=0, nullable=True)
    channel: ProductChannels

class ProductCreate(SQLModel):
    name: str = Field(max_length=50, min_length=1, nullable=False)
    current_price_online: Optional[Decimal] = Field(nullable=True, max_digits=10, decimal_places=3, ge=0)
    channel: ProductChannels

    @model_validator(mode='after')
    def check_current_price_online_matches_channel(self) -> Self:
        if (self.channel == 'Online Only' or self.channel == 'Both') and self.current_price_online == None: 
            raise ValueError('products available in online store should have a current price online')
        elif (self.channel == 'Offline Only' and self.current_price_online != None):
           raise ValueError('offline only products should not have online current prices stored')
        
        return self

# countries table api models
class CountryPublic(SQLModel):
    id: int = Field(nullable=False)
    name: str = Field(nullable=False, max_length=50, min_length=2)

class CountryCreate(SQLModel):
    name: str = Field(max_length=50, min_length=2)

# customers table api models
class CustomerPublic(SQLModel):
    id: int = Field(nullable=False)
    username: str = Field(max_length=50, min_length=1, nullable=False)
    email: str = Field(max_length=100, min_length=2, nullable=False)
    name: str = Field(max_length=50, min_length=1, nullable=False)
    country_id: int = Field(nullable=False)
    country_name: str = Field(nullable=False)

class CustomerCreate(SQLModel):
    name: str = Field(max_length=50, min_length=1, nullable=False)
    username: str = Field(max_length=50, min_length=1, nullable=False)
    email: str = Field(max_length=100, min_length=2, nullable=False)
    country_id: int = Field(nullable=False)

# status table api models
class StatusPublic(SQLModel):
    id: int = Field(nullable=False)
    name: str = Field(max_length=50, min_length=1, nullable=False)

class StatusCreate(SQLModel):
    name: str = Field(max_length=50, min_length=1, nullable=False)

# order items api models
class OrderItemPublic(SQLModel):
    id: int = Field(nullable=False)
    product_id: int = Field(nullable=False)
    product_name: str = Field(max_length=50, min_length=1, nullable=False)
    order_id: int = Field(nullable=False)
    quantity: int = Field(nullable=False, ge=1)
    price_per_unit_at_purchase: FloatDecimal = Field(max_digits=10, decimal_places=3, ge=0, nullable=False)
    discount_per_unit_amount: FloatDecimal = Field(max_digits=10, decimal_places=3, ge=0, nullable=False)

class OrderItemCreate(SQLModel):
    quantity: int = Field(nullable=False, ge=0)
    product_id: int = Field(nullable=False)
    discount_per_unit_amount: Decimal = Field(max_digits=10, decimal_places=3, ge=0, nullable=False)

# orders table api models
class OrderPublic(SQLModel):
    id: int = Field(nullable=False)
    created_at: datetime = Field(nullable=False)
    status_last_updated_at: datetime = Field(nullable=False)
    current_status_id: int = Field(nullable=False)
    current_status_name: str = Field(max_length=50, min_length=1, nullable=False)
    customer_id: int = Field(nullable=False)
    customer_name: str = Field(max_length=50, min_length=1, nullable=False)
    tax_amount: FloatDecimal = Field(max_digits=10, decimal_places=3, ge=0)
    discount_off_order_amount: FloatDecimal = Field(max_digits=10, decimal_places=3, ge=0)
    shipping_costs_amount: FloatDecimal = Field(max_digits=10, decimal_places=3, ge=0)
    order_items: list[OrderItemPublic]

class OrderCreate(SQLModel):
    customer_id: int = Field(nullable=False)
    items: list[OrderItemCreate] = Field(nullable=False)
    tax_amount: Decimal = Field(max_digits=10, decimal_places=3, ge=0, nullable=False)
    discount_off_order_amount: Decimal = Field(max_digits=10, decimal_places=3, ge=0, nullable=False)
    shipping_costs_amount: Decimal = Field(max_digits=10, decimal_places=3, ge=0, nullable=False)

    # check if there are duplicated product IDs in the list of items purchased
    # throw error if they exist
    @field_validator('items', mode='after')  
    @classmethod
    def no_duplicate_product_id(cls, items: list):
       product_ids = [item.dict()['product_id'] for item in items]

       if len(product_ids) != len(set(product_ids)):
        raise ValueError("unexpected behavior detected: duplicated product IDs in one order")

       return items

    # check if there is at least an item to order, throw error if not
    @field_validator('items', mode='after')  
    @classmethod
    def items_to_order_exists(cls, items: list):
       if len(items) == 0 or items is None:
        raise ValueError("order should consists of at least one product to order")

       return items

    # check if there is an item with quantity of 0
    @field_validator('items', mode='after')  
    @classmethod
    def items_to_order_doesnt_have_qty_of_0(cls, items: list):
       product_quantities = [item.dict()['quantity'] for item in items]

       if 0 in product_quantities:
        raise ValueError("unexpected behavior detected: order item of quantity 0 found")

       return items

class OrderUpdate(SQLModel):
    current_status_id: int
    