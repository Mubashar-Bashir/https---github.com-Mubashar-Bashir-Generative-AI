# delete_user_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.user_model import User
import asyncio
import json
from app.crud.crud_user import delete_user_by_id, get_user_by_id
import logging
from app.settings import KAFKA_DELETE_USER_TOPIC
topic = KAFKA_DELETE_USER_TOPIC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_delete_user():
    logger.info("Step-1: consumer_delete_user: Called")

    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            logger.info(f"Step-2: consumer_delete_user: msg: {msg}")
            user_data = json.loads(msg.value.decode())  # Get the message value (deserialized JSON)
            logger.info(f"user Loaded: {user_data}")
            with (get_session()) as session:
                try:
                    
                    delete_user_by_id(int(user_data['id']), session=session)
                    logger.info(f"user Deleted: {user_data}")
                except Exception as e:
                    logger.error(f"Error while deleting user: {e}")
