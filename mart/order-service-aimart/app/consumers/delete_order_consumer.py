from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.order_model import Order  # Import Order model if needed
import asyncio
import json
from app.crud.crud_order import delete_order  # Import appropriate CRUD function
import logging
from app.order_settings import KAFKA_DELETE_ORDER_TOPIC

topic = KAFKA_DELETE_ORDER_TOPIC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_delete_order():
    logger.info("Consumer for deleting orders initialized.")

    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            try:
                order_data = json.loads(msg.value.decode())  # Deserialize JSON message
                order_id = order_data.get('order_id')  # Extract order_id from message
                print("Delete Consumer find job from kafka to delet id >>>>",order_id)
                with get_session() as session:
                    delete_order(order_id=order_id, session=session)
                    logger.info(f"Deleted order with id: {order_id}")

            except Exception as e:
                logger.error(f"Error processing delete request: {e}")
