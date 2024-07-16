# delete_product_producer.py
from app.producers.kafka_producer import get_kafka_producer
from app.settings import KAFKA_DELETE_PRODUCT_TOPIC

async def send_delete_product(product_id):
    async with get_kafka_producer() as producer:
        await producer.send("delete-product", {"id": product_id})
        await producer.flush()
