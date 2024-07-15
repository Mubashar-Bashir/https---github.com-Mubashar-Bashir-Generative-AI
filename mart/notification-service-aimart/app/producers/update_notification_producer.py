from app.producers.kafka_producer import get_kafka_producer
from app.notification_settings import KAFKA_UPDATE_NOTIFICATION_TOPIC
from app.models.notification_model import NotificationUpdate  # Assuming notificationUpdate model is defined
import json

topic = KAFKA_UPDATE_NOTIFICATION_TOPIC

async def send_update_notification(notification_id: int, updated_notification_data: NotificationUpdate):
    # Create the message payload
    notification_update_payload = {
        "notification_id": notification_id,
        "update_data": updated_notification_data.dict(exclude_unset=True)
    }
    message_data = json.dumps(notification_update_payload).encode('utf-8')
    logger.info(f"Producer >>> Preparing to send update message: {message_data}")

    try:
        async for producer in get_kafka_producer():
            await producer.send_and_wait(topic, message_data)
            logger.info(f"Sent update message to topic {topic} for notification ID {notification_id}")
            return notification_update_payload
    except Exception as e:
        logger.error(f"Error sending update message to Kafka: {e}")
        return None