from app.producers.kafka_producer import get_kafka_producer
import json
from app.settings import BOOTSTRAP_SERVER, KAFKA_DELETE_PRODUCT_TOPIC
import logging
topic = KAFKA_DELETE_PRODUCT_TOPIC
import uuid

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

async def send_delete_product(product_id: uuid.UUID):
    jsonify_id = {
        "id": str(product_id)
    }
    product_json = json.dumps(jsonify_id).encode("utf-8")
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, product_json)
        
