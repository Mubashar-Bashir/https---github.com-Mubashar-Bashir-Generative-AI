# create_product_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.product_model import Product
import asyncio
import json
from app.settings import KAFKA_CREATE_PRODUCT_TOPIC
topic=KAFKA_CREATE_PRODUCT_TOPIC

async def consume_create_product():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            product_data = msg.value
            async with get_session() as session:
                product = Product(**product_data)
                session.add(product)
                session.commit()
                session.refresh(product)
