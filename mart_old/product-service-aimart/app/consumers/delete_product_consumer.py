# delete_product_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.product_model import Product
import asyncio
from sqlmodel import select
from app.settings import KAFKA_DELETE_PRODUCT_TOPIC
topic=KAFKA_DELETE_PRODUCT_TOPIC

async def consume_delete_product():
    # Use the get_kafka_consumer function to create a consumer for the "delete-product-topic"
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            product_data = msg.value  # Get the message value (deserialized JSON)
            async with get_session() as session:
                statement = select(Product).where(Product.id == product_data['id'])
                results = session.exec(statement)
                product = results.one_or_none()
                if product:
                    session.delete(product)
                    session.commit()
                    session.refresh(product)
