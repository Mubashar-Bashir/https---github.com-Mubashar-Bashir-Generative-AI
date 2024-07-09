# delete_inventory_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.inventory_model import Inventory
import asyncio
import json
from app.crud.crud_inventory import delete_inventory_by_id
import logging
from app.settings import KAFKA_DELETE_INVENTORY_TOPIC

topic = KAFKA_DELETE_INVENTORY_TOPIC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_delete_inventory():
    logger.info("Step-1: consumer_delete_inventory: Called")

    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            logger.info(f"Step-2: consumer_delete_inventory: msg: {msg}")
            inventory_data = json.loads(msg.value.decode())  # Get the message value (deserialized JSON)
            logger.info(f"Inventory Loaded: {inventory_data}")
            with get_session() as session:
                try:
                    delete_inventory_by_id(int(inventory_data['id']), session=session)
                    logger.info(f"Inventory Deleted: {inventory_data}")
                except Exception as e:
                    logger.error(f"Error while deleting inventory: {e}")
