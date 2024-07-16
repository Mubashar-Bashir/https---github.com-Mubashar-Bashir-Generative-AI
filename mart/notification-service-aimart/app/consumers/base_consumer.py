from aiokafka import AIOKafkaConsumer
import json
# from app.notification_settings import KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION, BOOTSTRAP_SERVER, KAFKA_CONSUMER_GROUP_ID_FOR_ORDER
from app.notification_settings import (
    BOOTSTRAP_SERVER, 
    KAFKA_CREATE_ORDER_TOPIC, 
    KAFKA_UPDATE_ORDER_TOPIC, 
    KAFKA_DELETE_ORDER_TOPIC, 
    KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
    KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION
)
kafka_group = KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION
kafka_group_order = KAFKA_CONSUMER_GROUP_ID_FOR_ORDER

async def get_kafka_consumer(*topics):
    consumer = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=BOOTSTRAP_SERVER,
        group_id=kafka_group,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        auto_commit_interval_ms=1000,
        session_timeout_ms=6000,  # Adjust as needed
        heartbeat_interval_ms=2000,  # Adjust as needed
        # value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()
    try:
        yield consumer
    finally:
        await consumer.stop()

topics = ["Create_ORDER_Events", "Update_ORDER_Events", "Delete_ORDER_Events"]
async def get_kafka_order_consumer(*topics):
    consumer = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=BOOTSTRAP_SERVER,
        group_id=KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        # bootstrap_servers=BOOTSTRAP_SERVER,
        # group_id=kafka_group_order,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        # auto_commit_interval_ms=1000,
        # session_timeout_ms=6000,  # Adjust as needed
        # heartbeat_interval_ms=2000,  # Adjust as needed
        # value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()
    try:
        yield consumer
    finally:
        await consumer.stop()
