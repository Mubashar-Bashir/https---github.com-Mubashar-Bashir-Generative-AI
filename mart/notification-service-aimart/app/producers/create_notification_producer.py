#send_create_notification.py
from app.producers.kafka_producer import get_kafka_producer
from app.notification_settings import KAFKA_CREATE_NOTIFICATION_TOPIC  # Assuming this is defined in settings
import asyncio
import logging

topic = KAFKA_CREATE_NOTIFICATION_TOPIC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def send_create_notification(notification_json):
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, notification_json)
        # return notification_json