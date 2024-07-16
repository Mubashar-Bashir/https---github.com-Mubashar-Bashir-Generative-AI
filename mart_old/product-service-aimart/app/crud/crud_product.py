# app/consumers/add_product_consumer.py
from aiokafka import AIOKafkaConsumer
import json
from fastapi import HTTPException
from app.db_c_e_t_session import get_session
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
                    add_new_product(product_data, session)
                elif message.topic == UPDATE_PRODUCT_TOPIC:
                    update_product(product_data, session)
                elif message.topic == DELETE_PRODUCT_TOPIC:
                    delete_product(product_data, session)
    finally:
        await consumer.stop()
# Remove this line to avoid circular import
# from app.crud.crud_product import add_new_product, update_product, delete_product

from sqlmodel import Session
from app.models.product_model import Product

def add_new_product(session: Session, product_data: dict):
    product = Product(**product_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def update_product(session: Session, product_id: int, product_data: dict):
    product = session.get(Product, product_id)
    if product:
        for key, value in product_data.items():
            setattr(product, key, value)
        session.add(product)
        session.commit()
        session.refresh(product)
    return product

def delete_product(session: Session, product_id: int):
    product = session.get(Product, product_id)
    if product:
        session.delete(product)
        session.commit()
    return product
