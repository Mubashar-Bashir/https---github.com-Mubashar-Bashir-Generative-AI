from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.notification_model import notification, notificationUpdate  # Import notification model if needed
import asyncio
from app.crud.crud_notification import update_notification # Import appropriate CRUD function
import json
from app.notification_settings import KAFKA_SEND_NOTIFICATION_TOPIC

topic = KAFKA_SEND_NOTIFICATION_TOPIC

async def consume_update_notification():
    async for consumer in get_kafka_consumer(topic):
        async for msg in consumer:
            try:
                message_data = json.loads(msg.value.decode())  # Deserialize JSON message
                notification_id = message_data.get('notification_id')  # Extract notification_id from message
                update_data = notificationUpdate(**message_data.get('update_data'))  # Extract update_data from message

                with get_session() as session:
                    updated_notification = update_notification(session=session, notification_id=notification_id, notification_update=update_data)
                    if updated_notification:
                        print(f"Updated notification with id: {notification_id}")
                    else:
                        print(f"notification with id {notification_id} not found.")
                        
            except Exception as e:
                print(f"Error processing update request: {e}")