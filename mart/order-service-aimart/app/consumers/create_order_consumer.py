from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.order_model import Order
import asyncio
import json
from app.crud.crud_order import create_order
from app.order_settings import KAFKA_CREATE_ORDER_TOPIC
import logging

topic = KAFKA_CREATE_ORDER_TOPIC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def consume_create_order():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            order_data = json.loads(msg.value.decode())
            logger.info(f"Consumer received order data: {order_data}")
            try:
                with get_session() as session:
                    create_order(session=session, order=Order(**order_data))
                    logger.info(f"Order created successfully: {order_data}")
            except Exception as e:
                logger.error(f"Error creating order: {e}")

if __name__ == "__main__":
    asyncio.run(consume_create_order())
