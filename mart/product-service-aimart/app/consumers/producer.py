from aiokafka import AIOKafkaProducer
import json
from fastapi import Depends

async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers='broker:19092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def send_create_product(product, producer: AIOKafkaProducer):
    await producer.send('create-product', product)
    await producer.flush()

async def send_update_product(product, producer: AIOKafkaProducer):
    await producer.send('update-product', product)
    await producer.flush()

async def send_delete_product(product_id, producer: AIOKafkaProducer):
    await producer.send('delete-product', {'id': product_id})
    await producer.flush()
