# from app.consumers.base_consumer import get_kafka_consumer
# from app.db_c_e_t_session import get_session
# from app.models.notification_model import Notification
# import asyncio
# import json
# from app.crud.crud_notification import create_notification
# from app.notification_settings import KAFKA_CREATE_NOTIFICATION_TOPIC
# import logging
# from app.gateways.gmail_gateway import send_email_gmail

# topic = KAFKA_CREATE_NOTIFICATION_TOPIC

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)



# def parse_datetime_fields(data):
#     for field in ['sent_at', 'created_at', 'updated_at']:
#         if field in data and data[field]:
#             try:
#                 data[field] = datetime.fromisoformat(data[field])
#             except ValueError as e:
#                 logger.error(f"Error parsing datetime field '{field}': {e}")
#     return data

# async def consume_create_notification():
#     logger.info("Starting the simple_consume function")
#     async for consumer in get_kafka_consumer(topic):
#         logger.info("Connected to Kafka consumer")
#         async for msg in consumer:
#             notification_data = json.loads(msg.value.decode())
#             try:
#                 with get_session() as session:
#                     create_notification(session=get_session(), notification=notification_data)
#                     logger.info(f"Database stored notification data: {notification_data}")
#             except Exception as e:
#                 logger.error(f"Error storing notification data: {e}")
# if __name__ == "__main__":
#     asyncio.run(simple_consume())

# # async def consume_create_notification():
# #     print("I am in Consumer crete notification")

from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.notification_model import Notification
import asyncio
import json
from app.crud.crud_notification import create_notification
from app.notification_settings import KAFKA_CREATE_NOTIFICATION_TOPIC
import logging
from app.gateways.gmail_gateway import send_email_gmail
from datetime import datetime

topic = KAFKA_CREATE_NOTIFICATION_TOPIC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def parse_datetime_fields(data):
    for field in ['sent_at', 'created_at', 'updated_at']:
        if field in data and data[field]:
            try:
                data[field] = datetime.fromisoformat(data[field])
            except ValueError as e:
                logger.error(f"Error parsing datetime field '{field}': {e}")
    return data

async def consume_create_notification():
    logger.info("Starting the consume_create_notification function")
    async for consumer in get_kafka_consumer(topic):
        logger.info("Connected to Kafka consumer")
        async for msg in consumer:
            notification_data = json.loads(msg.value.decode())
            # logger.info(f"Received raw notification data: {notification_data}")
            notification_data = parse_datetime_fields(notification_data)
            # logger.info(f"Parsed notification data: {notification_data}")
            msg_to = notification_data.get("user_email")
            msg_username = notification_data.get("user_name")
            # logger.info(f"Consumer received notification data: {notification_data}")

            try:
                with get_session() as session:
                    created_notification = create_notification(session=session, notification=Notification(**notification_data))
                    if created_notification:
                        logger.info(f"Created notification in DB: {created_notification}")
                        logger.info(f"I am sending an Email to >>>> {msg_to}")
                        logger.info(f"From UserName >>>>> {msg_username}")
                        await send_email_gmail(
                            from_email="mubasharbashir003@gmail.com",
                            to_emails=msg_to,
                            subject=f"Notification created by: {msg_username}",
                            message=str(notification_data)
                        )
                        logger.info(f"Email sent successfully to {msg_to}")
            except Exception as e:
                logger.error(f"Error creating notification or sending email: {e}")

if __name__ == "__main__":
    asyncio.run(consume_create_notification())
