from app.producers.kafka_producer import get_kafka_producer
from app.payment_settings import KAFKA_UPDATE_PAYMENT_TOPIC
from app.models.payment_model import PaymentUpdate  # Assuming paymentUpdate model is defined
import json

topic = KAFKA_UPDATE_PAYMENT_TOPIC

async def send_update_payment(payment_id: int, updated_payment_data: PaymentUpdate):
    try:
        message_data = {
            "payment_id": payment_id,
            "update_data": updated_payment_data.dicr()
        }
         # Convert datetime fields to string
        if 'updated_at' in message_data['update_data'] and message_data['update_data']['updated_at']:
            message_data['update_data']['updated_at'] = message_data['update_data']['updated_at'].isoformat()
        
        message = json.dumps(message_data).encode('utf-8')
        print("Producer >>> message: id and updated value>>>>>>", message)
        async for producer in get_kafka_producer():
            await producer.send_and_wait(topic, value=message)
        
        print(f"Sent update request for payment id '{payment_id}' to Kafka topic '{topic}'")
    except Exception as e:
        print(f"Error sending update request for payment id '{payment_id}' to Kafka: {e}")
