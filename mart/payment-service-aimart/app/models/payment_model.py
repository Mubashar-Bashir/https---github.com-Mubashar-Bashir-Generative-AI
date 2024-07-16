from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Payment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    order_id: int
    customer_id: int
    amount: float
    currency: str = Field(default="USD", max_length=3)
    payment_status: str = Field(default="pending", max_length=50)
    stripe_payment_id: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Change made here
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else v
        }

class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    customer_id: Optional[int] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    payment_status: Optional[str] = None
    stripe_payment_id: Optional[str] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if isinstance(v, datetime) else v
        }
