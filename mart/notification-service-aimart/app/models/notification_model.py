from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator

class Notification(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int
    user_name: str
    user_email: str
    order_id: Optional[int] = None
    message: str
    notification_type: str
    is_sent: bool = False
    sent_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class NotificationCreate(BaseModel):
    user_id: int
    user_name: str
    order_id: Optional[int] = None
    user_email: str
    message: str
    notification_type: str
    is_sent: Optional[bool] = False
    sent_at: datetime
    created_at: datetime
    updated_at: datetime

    @validator('sent_at', 'created_at', 'updated_at', pre=True, always=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class NotificationUpdate(BaseModel):
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    order_id: Optional[int] = None
    user_email: Optional[str] = None
    message: Optional[str] = None
    notification_type: Optional[str] = None
    is_sent: Optional[bool] = None
    sent_at: Optional[datetime] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @validator('sent_at', 'updated_at', pre=True, always=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
