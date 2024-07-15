#delete_notification_produer
from app.producers.kafka_producer import get_kafka_producer
import json
from app.notification_settings import KAFKA_DELETE_NOTIFICATION_TOPIC

topic = KAFKA_DELETE_NOTIFICATION_TOPIC

async def send_delete_notification(notification_id: int):
    print("I am in delete producer Message to Kafka ")
    try:
        payload = {
            "notification_id": notification_id
        }
        notification_json = json.dumps(payload).encode("utf-8")
        
        async for producer in get_kafka_producer():
            await producer.send_and_wait(topic, value=notification_json)
        
        print(f"Producer Sent delete request for notification id '{notification_id}' to Kafka topic '{topic}'")
    except Exception as e:
        print(f"Error sending delete request for notification id '{notification_id}' to Kafka: {e}")

