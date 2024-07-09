# update_inventory_producer.py
from app.producers.kafka_producer import get_kafka_producer
from app.settings import KAFKA_UPDATE_INVENTORY_TOPIC
from app.models.inventory_model import InventoryUpdate
import json

topic = KAFKA_UPDATE_INVENTORY_TOPIC

async def send_update_inventory(inventory_id: int, to_update_inventory_data: InventoryUpdate):
    message_data = {
        "id": inventory_id,
        "update_data": to_update_inventory_data.dict()
    }
    message = json.dumps(message_data).encode('utf-8')
    print("Producer >>> message: id and updated value>>>>>>", message)
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, message)
        # await producer.flush()
