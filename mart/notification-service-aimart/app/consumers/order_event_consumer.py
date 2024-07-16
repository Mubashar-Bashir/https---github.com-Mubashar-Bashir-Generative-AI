import asyncio
import json
import logging
from datetime import datetime
from app.consumers.base_consumer import get_kafka_order_consumer
from app.crud.crud_notification import create_notification
from app.models.notification_model import NotificationCreate
from app.db_c_e_t_session import get_session
from app.gateways.gmail_gateway import send_email_gmail
from app.notification_settings import KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,KAFKA_CREATE_ORDER_TOPIC,KAFKA_DELETE_ORDER_TOPIC,KAFKA_UPDATE_ORDER_TOPIC

# topics = ["Create_ORDER_Events", "Update_ORDER_Events", "Delete_ORDER_Events"]
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# async def consume_order_events():
#     topics = [Create_ORDER_Events, Update_ORDER_Events, Delete_ORDER_Events]
#     async for consumer in get_kafka_order_consumer(*topics):
#         async for msg in consumer:
#             await process_message(msg)
topics = [KAFKA_CREATE_ORDER_TOPIC, KAFKA_UPDATE_ORDER_TOPIC, KAFKA_DELETE_ORDER_TOPIC]
async def consume_create_order():
    async for consumer in get_kafka_order_consumer(*topics):
        async for msg in consumer:
            await process_message(msg)
async def process_message(msg):
    topic = msg.topic
    value = msg.value
    print("Topic = >>>>>>>",topic)
    print("Value = >>>>>",value)

    if topic == Create_ORDER_Events:
        print("Selected Topic with condition >>>",topic)
        await handle_create_order(value)
    elif topic == Update_ORDER_Events:
        print("Selected Topic with condition >>>",topic)
        await handle_update_order(value)
    elif topic == Delete_ORDER_Events:
        print("Selected Topic with condition >>>",topic)
        await handle_delete_order(value)

async def handle_create_order(order_data):
    user_id = order_data['user_id']
    user_name = order_data['user_name']
    user_email = order_data['user_email']
    order_id = order_data['order_id']

    message = f"Order {order_id} has been created successfully."

    notification = NotificationCreate(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        order_id=order_id,
        message=message,
        notification_type="Order Created",
        is_sent=False,
        sent_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    try:
        with get_session() as session:
            create_notification(session, notification)
            print("Created Notification for DB {notification_type}>>>", notification.notification_type)
 
    except Exception as e:
        logger.error(e)
    # async with get_session() as session:
       
    await send_email_gmail(user_email, "Order Created", message)
    print("Email sent TO >>> ", user_email)

async def handle_update_order(order_data):
    user_id = order_data['user_id']
    user_name = order_data['user_name']
    user_email = order_data['user_email']
    order_id = order_data['order_id']

    message = f"Order {order_id} has been updated successfully."

    notification = NotificationCreate(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        order_id=order_id,
        message=message,
        notification_type="Order Updated",
        is_sent=False,
        sent_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

        # async with get_session() as session:
        #     await create_notification(session, notification)
        #     print("Created Notification {notification_type}>>>", notification.notification_type)
    try:
        with get_session() as session:
            create_notification(session, notification)
            print("Created Notification for DB {notification_type}>>>", notification.notification_type)
 
    except Exception as e:
        logger.error(e)
    await send_email_gmail(user_email, "Order Updated", message)
    print("Email sent TO >>> ", user_email)

async def handle_delete_order(order_data):
    user_id = order_data['user_id']
    user_name = order_data['user_name']
    user_email = order_data['user_email']
    order_id = order_data['order_id']

    message = f"Order {order_id} has been deleted successfully."

    notification = NotificationCreate(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        order_id=order_id,
        message=message,
        notification_type="Order Deleted",
        is_sent=False,
        sent_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # async with get_session() as session:
    #     await create_notification(session, notification)
    #     print(f"created notification for {notification.notification_type}>>>", notification.notification_type)
    try:
        with get_session() as session:
            create_notification(session, notification)
            print("Created Notification for DB {notification_type}>>>", notification.notification_type)
 
    except Exception as e:
        logger.error(e)
    await send_email_gmail(user_email, "Order Deleted", message)
    print(f"Email Has been Sent at {notification.user_email} >>> ", notification.user_email)
    print(f"Email Has been Sent at {notification.user_name} >>> ", notification.user_name)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    consumer_tasks = [
        asyncio.create_task(consume_create_order()),
        # asyncio.create_task(consume_update_order()),  # Define these functions if needed
        # asyncio.create_task(consume_delete_order())
    ]
    loop.run_until_complete(asyncio.wait(consumer_tasks))