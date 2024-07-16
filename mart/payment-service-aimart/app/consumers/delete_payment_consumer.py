from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.payment_model import Payment  # Import payment model if needed
import asyncio
import json
from app.crud.crud_payment import delete_payment  # Import appropriate CRUD function
import logging
from app.payment_settings import KAFKA_DELETE_PAYMENT_TOPIC

topic = KAFKA_DELETE_PAYMENT_TOPIC

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_delete_payment():
    logger.info("Consumer for deleting payments initialized.")

    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            try:
                payment_data = json.loads(msg.value.decode())  # Deserialize JSON message
                payment_id = payment_data.get('payment_id')  # Extract payment_id from message
                print("Delete Consumer find job from kafka to delet id >>>>",payment_id)
                with get_session() as session:
                    delete_payment(payment_id=payment_id, session=session)
                    logger.info(f"Deleted payment with id: {payment_id}")

            except Exception as e:
                logger.error(f"Error processing delete request: {e}")
