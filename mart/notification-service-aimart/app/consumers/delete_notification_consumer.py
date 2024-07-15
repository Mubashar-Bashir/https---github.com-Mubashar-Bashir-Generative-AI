from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.notification_model import Notification  # Import notification model if needed
import asyncio
import json
from app.crud.crud_notification import delete_notification  # Import appropriate CRUD function
import logging
from app.notification_settings import KAFKA_DELETE_NOTIFICATION_TOPIC

topic = KAFKA_DELETE_NOTIFICATION_TOPIC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_delete_notification():
    logger.info("Consumer for deleting notifications initialized.")

    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            try:
                notification_data = json.loads(msg.value.decode())  # Deserialize JSON message
                notification_id = notification_data.get('notification_id')  # Extract notification_id from message
                print("Delete Consumer find job from kafka to delet id >>>>",notification_id)
                with get_session() as session:
                    delete_notification(notification_id=notification_id, session=session)
                    logger.info(f"Deleted notification with id: {notification_id}")

            except Exception as e:
                logger.error(f"Error processing delete request: {e}")
