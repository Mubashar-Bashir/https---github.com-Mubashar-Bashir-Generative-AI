#send_create_payment.py
from app.producers.kafka_producer import get_kafka_producer
from app.payment_settings import KAFKA_CREATE_PAYMENT_TOPIC  # Assuming this is defined in settings
import asyncio
import logging

topic = KAFKA_CREATE_PAYMENT_TOPIC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def send_create_payment(payment_json):
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, payment_json)
        return payment_json