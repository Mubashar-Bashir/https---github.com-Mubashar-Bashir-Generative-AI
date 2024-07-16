from typing import List, Optional
from sqlmodel import Session, select
from app.models.payment_model import Payment, PaymentUpdate
from app.db_c_e_t_session import get_session
from sqlalchemy.sql import func  # Import func from sqlalchemy.sql

def create_payment(session: Session, payment: Payment) -> Payment:
    with session as session:
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment

def get_payment_by_id(session: Session, payment_id: int) -> Payment:
    with session as session:
        payment = session.get(Payment, payment_id)
        print("I found payment in payment Crud>>>>>",payment)
        return payment

def get_all_payments(session: Session) -> List[Payment]:
    with session as session:
        payments = session.exec(select(Payment)).all()
        return payments


def update_payment(session: Session, payment_id: int, payment_update: PaymentUpdate) -> Optional[Payment]:
    with session as session:
        payment = session.get(Payment, payment_id)
        if payment:
            payment_data = payment_update.dict(exclude_unset=True)
            for key, value in payment_data.items():
                setattr(payment, key, value)
            session.add(payment)
            session.commit()
            session.refresh(payment)
            return Payment
        return None


def delete_payment(session: Session, payment_id: int) -> bool:
    # with session as session:
        payment = session.get(Payment, payment_id)
        print("i am in delete CRUD to perform deletion at {payment_id} >>>>",payment)
        if payment:
            session.delete(payment)
            session.commit()
            return True
        return False

def count_all_payments() -> int:
    with get_session() as session:
        # Use select to count all payment entries
        count_query = select(func.count(Payment.id))
        result = session.exec(count_query).one()
        return result
