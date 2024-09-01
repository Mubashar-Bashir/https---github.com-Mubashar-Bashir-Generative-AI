import json
from aiokafka import AIOKafkaConsumer
from app.notification_settings import (
    BOOTSTRAP_SERVER,
    KAFKA_CREATE_PRODUCT_TOPIC,
    KAFKA_UPDATE_PRODUCT_TOPIC,
    KAFKA_DELETE_PRODUCT_TOPIC,
    KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT
)
from app.gateways.gmail_gateway import send_email_gmail  # Assuming you have an email sending utility

async def get_kafka_product_consumer():
    consumer = AIOKafkaConsumer(
        KAFKA_CREATE_PRODUCT_TOPIC,
        KAFKA_UPDATE_PRODUCT_TOPIC,
        KAFKA_DELETE_PRODUCT_TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVER,
        group_id=KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for msg in consumer:
            await handle_product_event(msg)
    finally:
        await consumer.stop()

async def handle_product_event(msg):
    event_type = msg.topic
    product_data = msg.value

    if event_type == KAFKA_CREATE_PRODUCT_TOPIC:
        subject = "New Product Created"
        message = f"A new product has been created: {product_data}"
    elif event_type == KAFKA_UPDATE_PRODUCT_TOPIC:
        subject = "Product Updated"
        message = f"Product has been updated: {product_data}"
    elif event_type == KAFKA_DELETE_PRODUCT_TOPIC:
        subject = "Product Deleted"
        message = f"A product has been deleted: {product_data}"
    else:
        return  # Unknown event type, no action taken

    # Send email notification
    await send_email_gmail(subject=subject, message=message)

