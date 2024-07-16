# app/consumers/add_product_consumer.py
from aiokafka import AIOKafkaConsumer
import json
from fastapi import HTTPException
from app.db_c_e_t_session import get_session
from app.crud.crud_product import add_new_product, update_product, delete_product
from app.models.product_model import Product
from app.consumers.config import KAFKA_BROKER_URL, ADD_PRODUCT_TOPIC, UPDATE_PRODUCT_TOPIC, DELETE_PRODUCT_TOPIC

async def consume_messages():
    consumer = AIOKafkaConsumer(
        ADD_PRODUCT_TOPIC,
        UPDATE_PRODUCT_TOPIC,
        DELETE_PRODUCT_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        group_id="product-group",
        auto_offset_reset="earliest",
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message on topic {message.topic}")

            product_data = json.loads(message.value.decode())
            with next(get_session()) as session:
                if message.topic == ADD_PRODUCT_TOPIC:
                    process_add_product(product_data, session)
                elif message.topic == UPDATE_PRODUCT_TOPIC:
                    process_update_product(product_data, session)
                elif message.topic == DELETE_PRODUCT_TOPIC:
                    process_delete_product(product_data, session)
    finally:
        await consumer.stop()

def process_add_product(product_data, session):
    try:
        db_insert_product = add_new_product(
            product_item_data=Product(**product_data), 
            session=session
        )
        print("Product added to database:", db_insert_product)
    except Exception as e:
        session.rollback()
        print("Failed to add product:", e)
        raise HTTPException(status_code=500, detail=str(e))

def process_update_product(product_data, session):
    try:
        db_update_product = update_product(
            product_item_data=Product(**product_data), 
            session=session
        )
        print("Product updated in database:", db_update_product)
    except Exception as e:
        session.rollback()
        print("Failed to update product:", e)
        raise HTTPException(status_code=500, detail=str(e))

def process_delete_product(product_data, session):
    try:
        product_id = product_data.get("id")
        if product_id is None:
            raise HTTPException(status_code=400, detail="Product ID is required for deletion")
        db_delete_product = delete_product(
            product_id=product_id, 
            session=session
        )
        print("Product deleted from database:", db_delete_product)
    except Exception as e:
        session.rollback()
        print("Failed to delete product:", e)
        raise HTTPException(status_code=500, detail=str(e))
