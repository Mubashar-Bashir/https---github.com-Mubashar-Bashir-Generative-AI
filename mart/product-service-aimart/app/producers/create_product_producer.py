# create_product_producer.py
from app.producers.kafka_producer import get_kafka_producer
from app.settings import KAFKA_CREATE_PRODUCT_TOPIC
from app.models.product_model import ProductAdd
from app.crud.crud_product import get_by_id
topic=KAFKA_CREATE_PRODUCT_TOPIC
async def send_create_product(product:ProductAdd):
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, product)
        return product
