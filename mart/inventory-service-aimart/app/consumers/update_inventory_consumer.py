# update_inventory_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.inventory_model import Inventory
import asyncio
from sqlmodel import select
from app.crud.crud_inventory import update_inventory
import json
from app.settings import KAFKA_UPDATE_INVENTORY_TOPIC

topic = KAFKA_UPDATE_INVENTORY_TOPIC

async def consume_update_inventory():
    # Use the get_kafka_consumer function to create a consumer for the "update-inventory-topic"
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            message_data = json.loads(msg.value.decode())  # Get the message value (deserialized JSON)
            print("update_consumer_received Data>>>>>>", message_data)
            inventory_id = message_data['id']
            update_data = message_data['update_data']
            with get_session() as session:
                try:
                    updated_inventory = update_inventory(session, inventory_id, update_data)                    
                    if updated_inventory:
                        print(f"Inventory with ID {inventory_id} updated successfully.")
                    else:
                        print(f"Inventory with ID {inventory_id} not found.")
                except Exception as e:
                    session.rollback()
                    print(f"Error during update: {e}")
                finally:
                    session.close()
