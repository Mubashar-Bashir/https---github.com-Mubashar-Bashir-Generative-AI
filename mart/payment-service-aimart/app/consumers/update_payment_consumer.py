from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.payment_model import Payment, PaymentUpdate  # Import payment model if needed
import asyncio
from app.crud.crud_payment import update_payment # Import appropriate CRUD function
import json
from app.payment_settings import KAFKA_UPDATE_PAYMENT_TOPIC

topic = KAFKA_UPDATE_PAYMENT_TOPIC

async def consume_update_payment():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            try:
                message_data = json.loads(msg.value.decode())  # Deserialize JSON message
                payment_id = message_data.get('payment_id')  # Extract payment_id from message
                update_data = paymentUpdate(**message_data.get('update_data'))  # Extract update_data from message

                with get_session() as session:
                    updated_payment = update_payment(session=session, payment_id=payment_id, payment_update=update_data)
                    if updated_payment:
                        print(f"Updated payment with id: {payment_id}")
                    else:
                        print(f"payment with id {payment_id} not found.")
                        
            except Exception as e:
                print(f"Error processing update request: {e}")