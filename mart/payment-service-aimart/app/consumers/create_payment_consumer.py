from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.payment_model import Payment
import asyncio
import json
from app.crud.crud_payment import create_payment
from app.payment_settings import KAFKA_CREATE_PAYMENT_TOPIC
import logging

topic = KAFKA_CREATE_PAYMENT_TOPIC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def consume_create_payment():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            payment_data = json.loads(msg.value.decode("utf-8"))
            logger.info(f"Consumer received payment data: >>>>>> {payment_data}")
            try:
                with get_session() as session:
                    create_payment(session=session, payment=Payment(**payment_data))
                    logger.info(f"payment created successfully:>>>>>> {payment_data}")
            except Exception as e:
                logger.error(f"Error creating payment: {e}")

if __name__ == "__main__":
    asyncio.run(consume_create_payment())
