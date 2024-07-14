# create_user_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.user_model import User
import asyncio
import json
from app.crud.crud_user import create_user
from app.settings import KAFKA_CREATE_USER_TOPIC
topic=KAFKA_CREATE_USER_TOPIC
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_create_user():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            user_data = json.loads(msg.value.decode())
            logger.info(f"Consumer Received user data: {user_data}")
            try:
                with get_session() as session:
                    create_user(session=session, user_data=user_data)
                    logger.info(f"user created successfully: {user_data}")
            except Exception as e:
                logger.error(f"Error creating user: {e}")

            ########################
            # async for msg in consumer:
            #     print("I am in adding this value in db>>>>>>>",msg.value)
            #     user_data = json.loads(msg.value.decode())
            #     print("I am calling CRUD to Perfrom creation of ", user_data)
            #     add_new_user(session=session,user_data=user_data)
            