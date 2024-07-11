from typing import List, Optional
from sqlmodel import Session, select
from app.models.order_model import Order, OrderUpdate

def create_order(session: Session, order: Order) -> Order:
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_order(session: Session, order_id: int) -> Optional[Order]:
    order = session.get(Order, order_id)
    return order

def get_all_orders(session: Session) -> List[Order]:
    orders = session.exec(select(Order)).all()
    return orders

def update_order(session: Session, order_id: int, order_update: OrderUpdate) -> Optional[Order]:
    order = session.get(Order, order_id)
    if order:
        order_data = order_update.dict(exclude_unset=True)
        for key, value in order_data.items():
            setattr(order, key, value)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
    return None

def delete_order(session: Session, order_id: int) -> bool:
    order = session.get(Order, order_id)
    if order:
        session.delete(order)
        session.commit()
        return True
    return False
