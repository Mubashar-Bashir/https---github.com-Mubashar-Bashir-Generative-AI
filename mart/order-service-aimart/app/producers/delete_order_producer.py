#delete_order_produer
from app.producers.kafka_producer import get_kafka_producer
import json
from app.order_settings import KAFKA_DELETE_ORDER_TOPIC

topic = KAFKA_DELETE_ORDER_TOPIC

async def send_delete_order(order_id: int):
    print("I am in delete producer Message to Kafka ")
    try:
        payload = {
            "order_id": order_id
        }
        order_json = json.dumps(payload).encode("utf-8")
        
        async for producer in get_kafka_producer():
            await producer.send_and_wait(topic, value=order_json)
        
        print(f"Producer Sent delete request for order id '{order_id}' to Kafka topic '{topic}'")
    except Exception as e:
        print(f"Error sending delete request for order id '{order_id}' to Kafka: {e}")

