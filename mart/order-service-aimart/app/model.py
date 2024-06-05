from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: datetime
    
    user: User = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")