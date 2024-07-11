from app.producers.kafka_producer import get_kafka_producer
from app.order_settings import KAFKA_UPDATE_ORDER_TOPIC
from app.models.order_model import OrderUpdate  # Assuming OrderUpdate model is defined
import json

topic = KAFKA_UPDATE_ORDER_TOPIC

async def send_update_order(order_id: int, updated_order_data: OrderUpdate):
    try:
        message_data = {
            "order_id": order_id,
            "update_data": updated_order_data.dict()
        }
        message = json.dumps(message_data).encode('utf-8')
        
        async for producer in get_kafka_producer():
            await producer.send_and_wait(topic, value=message)
        
        print(f"Sent update request for order id '{order_id}' to Kafka topic '{topic}'")
    except Exception as e:
        print(f"Error sending update request for order id '{order_id}' to Kafka: {e}")
