from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    category_id: int = Field(foreign_key="category.id")
    
    category: Category = Relationship(back_populates="products")
    


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    products: List["Product"] = Relationship(back_populates="category")
