from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user_model import User