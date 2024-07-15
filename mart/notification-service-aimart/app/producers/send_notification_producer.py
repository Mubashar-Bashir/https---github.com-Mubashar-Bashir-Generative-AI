from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.notification_model import Notification, NotificationUpdate  # Import notification model if needed
import asyncio
from app.crud.crud_notification import update_notification # Import appropriate CRUD function
import json
from app.notification_settings import KAFKA_SEND_NOTIFICATION_TOPIC

topic = KAFKA_SEND_NOTIFICATION_TOPIC
