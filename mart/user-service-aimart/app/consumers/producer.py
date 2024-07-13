#producer.py
from aiokafka import AIOKafkaProducer
import json
from fastapi import Depends
from app.settings import BOOTSTRAP_SERVER,KAFKA_PRODUCT_TOPIC,KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT
BOOTSTRAP_SERVER=BOOTSTRAP_SERVER
topic=KAFKA_PRODUCT_TOPIC
consumer_group_id=KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT

async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def send_create_product(product, producer: get_kafka_producer):
    await producer.send("create-product", product)
    await producer.flush()

async def send_update_product(product, producer: get_kafka_producer):
    await producer.send('update-product', product)
    await producer.flush()

async def send_delete_product(product_id, producer: get_kafka_producer):
    await producer.send('delete-product', {'id': product_id})
    await producer.flush()
