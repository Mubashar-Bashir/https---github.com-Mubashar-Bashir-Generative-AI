# update_product_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.product_model import Product
import asyncio
from sqlmodel import select
from app.crud.crud_product import update_product
import json
from app.settings import KAFKA_UPDATE_PRODUCT_TOPIC
topic=KAFKA_UPDATE_PRODUCT_TOPIC

async def consume_update_product():
    # Use the get_kafka_consumer function to create a consumer for the "update-product-topic"
    async for consumer in get_kafka_consumer(topic):
        #print("I am in Conumer >>>> topic selected:",topic)
        async for msg in consumer:
            message_data = json.loads(msg.value.decode())  # Get the message value (deserialized JSON)
            print("update_consumer_received Data>>>>>>", message_data)
            product_id = str(message_data['id'])
            update_data = message_data['update_data']
            with (get_session()) as session:
                try:
                    updated_product = update_product(session, product_id, update_data)                    
                    if updated_product:
                        print(f"Product with ID {str(product_id)} updated successfully.")
                    else:
                        print(f"Product with ID {str(product_id)} not found.")
                except Exception as e:
                    session.rollback()
                    print(f"Error during update: {e}")
                finally:
                    session.close()