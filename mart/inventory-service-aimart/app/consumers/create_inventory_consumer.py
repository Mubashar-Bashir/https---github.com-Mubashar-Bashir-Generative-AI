# create_inventory_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.inventory_model import Inventory
import asyncio
import json
from app.crud.crud_inventory import add_new_inventory
from app.settings import KAFKA_CREATE_INVENTORY_TOPIC
import logging

topic = KAFKA_CREATE_INVENTORY_TOPIC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def consume_create_inventory():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            inventory_data = json.loads(msg.value.decode())
            logger.info(f"Consumer Received inventory data: {inventory_data}")
            try:
                with get_session() as session:
                    add_new_inventory(session=session, inventory_data=inventory_data)
                    logger.info(f"Inventory created successfully: {inventory_data}")
            except Exception as e:
                logger.error(f"Error creating inventory: {e}")
