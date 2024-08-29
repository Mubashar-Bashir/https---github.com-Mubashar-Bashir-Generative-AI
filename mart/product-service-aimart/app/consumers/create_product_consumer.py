# create_product_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.product_model import Product
import asyncio
import json
from app.crud.crud_product import add_new_product
from app.settings import KAFKA_CREATE_PRODUCT_TOPIC
topic=KAFKA_CREATE_PRODUCT_TOPIC
import logging
# import psycopg2  # or psycopg2-binary
# import psycopg2.errors  


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_create_product():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            product_data = json.loads(msg.value.decode())
            logger.info(f"Consumer Received product data: {product_data}")
            try:
                with get_session() as session:
                    add_new_product(session=session, product_data=product_data)
                    logger.info(f"Product created successfully: {product_data}")
            except Exception as e:
                print(f"Error creating product: {e}")
                # Consider logging or additional error handling

            ######################
            # async for msg in consumer:
            #     print("I am in adding this value in db>>>>>>>",msg.value)
            #     product_data = json.loads(msg.value.decode())
            #     print("I am calling CRUD to Perfrom creation of ", product_data)
            #     add_new_product(session=session,product_data=product_data)
            