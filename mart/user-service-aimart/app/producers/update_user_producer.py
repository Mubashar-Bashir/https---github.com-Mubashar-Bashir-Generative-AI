# update_user_producer.py
from app.producers.kafka_producer import get_kafka_producer
from app.settings import KAFKA_UPDATE_USER_TOPIC
from app.models.user_model import UserUpdate
import json
topic = KAFKA_UPDATE_USER_TOPIC

async def send_update_user(user_id: int, to_update_user_data: UserUpdate):
    message_data = {
        "id": user_id,
        "update_data": to_update_user_data.dict()
    }
    message = json.dumps(message_data).encode('utf-8')
    print("Producer >>> message: id and updated value>>>>>>", message)
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, message)
        # await producer.flush()