from app.producers.kafka_producer import get_kafka_producer
import json
from app.settings import BOOTSTRAP_SERVER, KAFKA_DELETE_USER_TOPIC
import logging
topic = KAFKA_DELETE_USER_TOPIC

# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

async def send_delete_user(user_id: int):
    jsonify_id = {
        "id": user_id
    }
    user_json = json.dumps(jsonify_id).encode("utf-8")
    async for producer in get_kafka_producer():
        await producer.send_and_wait(topic, user_json)
        return user_id
