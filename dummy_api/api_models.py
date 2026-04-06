from sqlmodel import Field, SQLModel, String
from decimal import Decimal
from pydantic import Field
from .db_models import DimensionsBase

class ProductPublic(DimensionsBase):
    id: int
    current_price: Decimal 

class ProductCreate(DimensionsBase):
    name: str = Field(max_length=100)
    current_price: Decimal = Field(max_digits=10, decimal_places=3)