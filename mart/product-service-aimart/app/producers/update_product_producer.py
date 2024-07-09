# update_product_producer.py
from app.producers.kafka_producer import get_kafka_producer
from app.settings import KAFKA_UPDATE_PRODUCT_TOPIC
from app.models.product_model import ProductUpdate
import json
topic = KAFKA_UPDATE_PRODUCT_TOPIC

async def send_update_product(product_id: int, to_update_product_data: ProductUpdate):
    message_data = {
        "id": product_id,
        "update_data": to_update_product_data.dict()
    }
    message = json.dumps(message_data).encode('utf-8')
    print("Producer >>> message: id and updated value>>>>>>", message)
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, message)
        # await producer.flush()