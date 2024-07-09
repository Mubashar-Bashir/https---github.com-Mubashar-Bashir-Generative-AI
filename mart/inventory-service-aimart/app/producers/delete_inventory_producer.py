# delete_inventory_producer.py
from app.producers.kafka_producer import get_kafka_producer
import json
from app.settings import BOOTSTRAP_SERVER, KAFKA_DELETE_INVENTORY_TOPIC

topic = KAFKA_DELETE_INVENTORY_TOPIC

async def send_delete_inventory(inventory_id: int):
    jsonify_id = {
        "id": inventory_id
    }
    inventory_json = json.dumps(jsonify_id).encode("utf-8")
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, inventory_json)
