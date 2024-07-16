# create_product_producer.py
from app.producers.kafka_producer import get_kafka_producer
from app.settings import KAFKA_CREATE_PRODUCT_TOPIC


async def send_create_product(product):
    async with get_kafka_producer() as producer:
        await producer.send("create-product", product)
        await producer.flush()
