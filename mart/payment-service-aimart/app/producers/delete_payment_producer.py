#delete_payment_produer
from app.producers.kafka_producer import get_kafka_producer
import json
from app.payment_settings import KAFKA_DELETE_PAYMENT_TOPIC

topic = KAFKA_DELETE_PAYMENT_TOPIC

async def send_delete_payment(payment_id: int):
    print("I am in delete producer Message to Kafka ")
    try:
        payload = {
            "payment_id": payment_id
        }
        payment_json = json.dumps(payload).encode("utf-8")
        
        async for producer in get_kafka_producer():
            await producer.send_and_wait(topic, value=payment_json)
        
        print(f"Producer Sent delete request for payment id '{payment_id}' to Kafka topic '{topic}'")
    except Exception as e:
        print(f"Error sending delete request for payment id '{payment_id}' to Kafka: {e}")

