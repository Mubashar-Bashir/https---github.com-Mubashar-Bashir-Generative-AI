# base_consumer.py
from aiokafka import AIOKafkaConsumer
import json
from app.settings import BOOTSTRAP_SERVER

async def get_kafka_consumer(*topics):
    consumer = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()
    try:
        yield consumer
    finally:
        await consumer.stop()
