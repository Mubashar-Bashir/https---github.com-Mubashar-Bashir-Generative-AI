from typing import List, Optional
from sqlmodel import Session, select
from app.models.order_model import Order, OrderUpdate
from app.db_c_e_t_session import get_session
from sqlalchemy.sql import func  # Import func from sqlalchemy.sql

def create_order(session: Session, order: Order) -> Order:
    with session as session:
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

def get_order_by_id(session: Session, order_id: int) -> Order:
    with session as session:
        order = session.get(Order, order_id)
        print("I found order in Order Crud>>>>>",order)
        return order

def get_all_orders(session: Session) -> List[Order]:
    with session as session:
        orders = session.exec(select(Order)).all()
        return orders

def update_order(session: Session, order_id: int, order_update: OrderUpdate) -> Optional[Order]:
    with session as session:
        order = session.get(Order, order_id)
        if order:
            order_data = order_update.dict(exclude_unset=True)
            for key, value in order_data.items():
                setattr(order, key, value)
            session.add(order)
            session.commit()
            session.refresh(order)
            return order.dict()
        # return None

def delete_order(session: Session, order_id: int) -> bool:
    with session as session:
        order = session.get(Order, order_id)
        if order:
            session.delete(order)
            session.commit()
            return True
        return False

def count_all_orders() -> int:
    with get_session() as session:
        # Use select to count all Order entries
        count_query = select(func.count(Order.id))
        result = session.exec(count_query).one()
        return result
