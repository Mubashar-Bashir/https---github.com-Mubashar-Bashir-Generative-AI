# create_user_producer.py
from app.producers.kafka_producer import get_kafka_producer
from app.settings import KAFKA_CREATE_USER_TOPIC
topic=KAFKA_CREATE_USER_TOPIC

async def send_create_user(user):
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, user)
        return user
