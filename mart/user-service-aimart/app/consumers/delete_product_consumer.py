# delete_product_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.product_model import Product
import asyncio
import json
from app.crud.crud_product import delete_product_by_id, get_by_id
import logging
from app.settings import KAFKA_DELETE_PRODUCT_TOPIC
topic = KAFKA_DELETE_PRODUCT_TOPIC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_delete_product():
    logger.info("Step-1: consumer_delete_product: Called")

    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            logger.info(f"Step-2: consumer_delete_product: msg: {msg}")
            product_data = json.loads(msg.value.decode())  # Get the message value (deserialized JSON)
            logger.info(f"Product Loaded: {product_data}")
            with (get_session()) as session:
                try:
                    
                    delete_product_by_id(int(product_data['id']), session=session)
                    logger.info(f"Product Deleted: {product_data}")
                except Exception as e:
                    logger.error(f"Error while deleting product: {e}")
