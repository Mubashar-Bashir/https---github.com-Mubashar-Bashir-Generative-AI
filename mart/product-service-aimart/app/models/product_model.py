#product_model.py schema
from sqlmodel import SQLModel, Field  # Import SQLModel and Field from SQLModel for ORM and field definitions
from pydantic import BaseModel
from typing import Optional # Import Annotated for type annotations

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category: Optional[str] = Field(default=None, index=True)
    
class ProductUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category: Optional[str] = Field(default=None, index=True)