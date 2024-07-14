# app/consumers/add_product_consumer.py
from sqlmodel import SQLModel, Field, Session, select, func
from typing import Optional, List
from app.models.user_model import User,UserUpdate
from app.db_c_e_t_session import get_session
# Create new user
def create_user(session: Session, user_data: dict) -> User:
     with session as session:
        user = User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

# Update user by ID
def update_user(session: Session, user_id: int, update_data) -> Optional[User]:
    print("I am in Crud update user")
    with session as session:
        user = session.get(User, user_id)
        if user:
            update_data = update_data.dict(exclude_unset=True)
            print("updated data>>>>>>",update_data)
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
    with session as session:
        user = session.get(User, user_id)
        print("I found User in CRUD >>>",user)
        return user
        # return session.get(User, user_id)

# Get all users
def get_all_users(session: Session) -> List[User]:
    with session as session:
        users = session.exec(select(User)).all()
        return users

def count_all_users() -> int:
    with get_session() as session:
        # Use select to count all Order entries
        count_query = select(func.count(User.id))
        result = session.exec(count_query).one()
        return result