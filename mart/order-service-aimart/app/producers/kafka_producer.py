 #kafka_producer.py
from aiokafka import AIOKafkaProducer
from app.order_settings import BOOTSTRAP_SERVER
import json

async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        # value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()