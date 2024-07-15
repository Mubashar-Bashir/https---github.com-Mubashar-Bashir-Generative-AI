#user_model.py schema
from sqlmodel import SQLModel, Field  # Import SQLModel and Field from SQLModel for ORM and field definitions
from pydantic import BaseModel
from typing import Optional  # Import Optional for optional fields

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    cell:str
    full_name: Optional[str] = None
    password_hash: str
    is_active: bool = True
    role: str = "user"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    cell: Optional[str] = None
    full_name: Optional[str] = None
    password_hash: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None