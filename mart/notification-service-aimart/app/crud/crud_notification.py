from typing import List, Optional
from sqlmodel import Session, select
from app.models.notification_model import Notification, NotificationUpdate,NotificationCreate
from app.db_c_e_t_session import get_session
from sqlalchemy.sql import func  # Import func from sqlalchemy.sql

def create_notification(session: Session, notification: Notification) -> Notification:
    with session as session:
        session.add(notification)
        session.commit()
        session.refresh(notification)
        return notification

def get_notification_by_id(session: Session, notification_id: int) -> Notification:
    with session as session:
        notification = session.get(Notification, notification_id)
        print("I found notification in Notification Crud>>>>>", notification)
        return notification

def get_all_notifications(session: Session) -> List[Notification]:
    with session as session:
        notifications = session.exec(select(Notification)).all()
        return notifications

def update_notification(session: Session, notification_id: int, notification_update: NotificationUpdate) -> Optional[Notification]:
    with session as session:
        notification = session.get(Notification, notification_id)
        if notification:
            notification_data = notification_update.dict(exclude_unset=True)
            for key, value in notification_data.items():
                setattr(notification, key, value)
            session.add(notification)
            session.commit()
            session.refresh(notification)
            return notification
        return None

def delete_notification(session: Session, notification_id: int) -> bool:
    with session as session:
        notification = session.get(Notification, notification_id)
        print(f"I am in delete CRUD to perform deletion at {notification_id} >>>>", notification)
        if notification:
            session.delete(notification)
            session.commit()
            return True
        return False

def count_all_notifications() -> int:
    with get_session() as session:
        # Use select to count all Notification entries
        count_query = select(func.count(Notification.id))
        result = session.exec(count_query).one()
        return result
