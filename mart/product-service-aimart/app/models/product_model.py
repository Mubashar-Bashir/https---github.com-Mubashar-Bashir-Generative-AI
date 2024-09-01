#product_model.py schema
from sqlmodel import SQLModel, Field  # Import SQLModel and Field from SQLModel for ORM and field definitions
from pydantic import BaseModel
from typing import Optional # Import Annotated for type annotations
from uuid import uuid4
import uuid
from uuid import UUID
class Product(SQLModel, table=True):
    # id: int = Field(default=None, primary_key=True)
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)  # Use UUID type
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = Field(default=None, index=True)
    
class ProductUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = Field(default=None, index=True)


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
