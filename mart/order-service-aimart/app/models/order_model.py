from sqlmodel import SQLModel, Field  # Import SQLModel and Field for ORM and field definitions
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int
    product_id: int
    quantity: int
    total_price: float
    order_status: str = Field(default="pending", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    total_price: Optional[float] = None
    order_status: Optional[str] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
