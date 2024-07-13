# app/consumers/add_product_consumer.py
from sqlmodel import SQLModel, Field, Session
from typing import Optional, List

# Create new user
def create_user(session: Session, user_data: dict) -> User:
    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Update user by ID
def update_user(session: Session, user_id: int, update_data: dict) -> Optional[User]:
    user = session.get(User, user_id)
    if user:
        for key, value in update_data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

# Delete user by ID
def delete_user_by_id(user_id: int, session: Session) -> Optional[dict]:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return {"message": f"User with id {user_id} deleted successfully."}
    return None

# Get user by ID
def get_user_by_id(user_id: int, session: Session) -> Optional[User]:
    return session.get(User, user_id)

# Get all users
def get_all_users(session: Session) -> List[User]:
    return session.exec(select(User)).all()