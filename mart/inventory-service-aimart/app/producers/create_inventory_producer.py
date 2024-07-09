
from app.producers.kafka_producer import get_kafka_producer
from app.settings import KAFKA_CREATE_INVENTORY_TOPIC  # Assuming this is defined in settings
from app.crud.crud_inventory import get_inventory_by_id

topic = KAFKA_CREATE_INVENTORY_TOPIC

async def send_create_inventory(inventory):
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, inventory)
        return inventory
