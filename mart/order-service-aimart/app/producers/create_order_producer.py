#send_create_order.py
from app.producers.kafka_producer import get_kafka_producer
from app.order_settings import KAFKA_CREATE_ORDER_TOPIC  # Assuming this is defined in settings
import asyncio
import logging

topic = KAFKA_CREATE_ORDER_TOPIC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def send_create_order(order):
    try:
        async for producer in get_kafka_producer():
            await producer.send(topic, value=order.encode())
            logger.info(f"Sent order data to Kafka topic '{topic}': {order}")
            return order
    except Exception as e:
        logger.error(f"Error sending order data to Kafka topic '{topic}': {e}")
