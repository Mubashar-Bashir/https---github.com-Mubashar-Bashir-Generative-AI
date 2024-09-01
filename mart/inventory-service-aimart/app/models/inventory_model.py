from sqlmodel import SQLModel, Field  # Import SQLModel and Field from SQLModel for ORM and field definitions
from pydantic import BaseModel
from typing import Optional  # Import Optional for type annotations

class Inventory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id:     int
    stock_quantity: int
    location:       Optional[str] = None  # location of Rack or warehouse location 

class InventoryUpdate(BaseModel):
    product_id:     int= None
    stock_quantity: int = None
    location:       str = None  # location warehouse location / Rack Location / Shop Store Number
