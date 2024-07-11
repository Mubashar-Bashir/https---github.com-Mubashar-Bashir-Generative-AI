from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.order_model import Order  # Import Order model if needed
import asyncio
from app.crud.crud_order import update_order # Import appropriate CRUD function
import json
from app.order_settings import KAFKA_UPDATE_ORDER_TOPIC

topic = KAFKA_UPDATE_ORDER_TOPIC

async def consume_update_order():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            try:
                message_data = json.loads(msg.value.decode())  # Deserialize JSON message
                order_id = message_data.get('order_id')  # Extract order_id from message
                update_data = message_data.get('update_data')  # Extract update_data from message

                with get_session() as session:
                    updated_order = update_order(order_id, update_data, session=session)
                    if updated_order:
                        print(f"Updated order with id: {order_id}")
                    else:
                        print(f"Order with id {order_id} not found.")
                        
            except Exception as e:
                print(f"Error processing update request: {e}")
