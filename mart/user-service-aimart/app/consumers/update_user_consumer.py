# update_user_consumer.py
from app.consumers.base_consumer import get_kafka_consumer
from app.db_c_e_t_session import get_session
from app.models.user_model import User,UserUpdate
import asyncio
from sqlmodel import select
from app.crud.crud_user import update_user
import json
from app.settings import KAFKA_UPDATE_USER_TOPIC
topic=KAFKA_UPDATE_USER_TOPIC

async def consume_update_user():
    # Use the get_kafka_consumer function to create a consumer for the "update-user-topic"
    async for consumer in get_kafka_consumer(topic):
        print("I am in Conumer >>>> topic selected:",topic)
        async for msg in consumer:
            try:
                message_data = json.loads(msg.value.decode())  # Get the message value (deserialized JSON)
                print("update_consumer_received Data>>>>>>", message_data)
                user_id = message_data.get('id')
                print("user id =",user_id)
               # Create a UserUpdate object and then convert it to a dictionary
                update_data = UserUpdate(**message_data.get('update_data'))
                print("update_data =", update_data)
                with get_session() as session:
                        updated_user = update_user(session=session, user_id=user_id, update_data=update_data)                    
                        if updated_user:
                            print(f"user with ID {user_id} updated successfully.")
                        else:
                            print(f"user with ID {user_id} not found.")
            except Exception as e:
                session.rollback()
                print(f"Error during update: {e}")
            finally:
                session.close()