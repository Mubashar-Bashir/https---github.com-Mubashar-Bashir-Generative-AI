
from typing import Annotated, List, Dict
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db_c_e_t_session import get_session, create_db_and_tables
import asyncio
from typing import AsyncGenerator
import json
from sqlmodel import SQLModel, Session,  select
# from app.consumers.add_product_consumer import consume_messages
from app.models.notification_model import Notification,NotificationUpdate, NotificationCreate
# app/main.py
from fastapi import FastAPI
from datetime import datetime
from app.crud.crud_notification import get_all_notifications,get_notification_by_id,create_notification,update_notification,delete_notification,count_all_notifications
#from app.consumers.producer import send_create_product, send_update_product, send_delete_product
#Producers
from app.producers.create_notification_producer import send_create_notification
from app.producers.update_notification_producer import send_update_notification
from app.producers.delete_notification_producer import send_delete_notification
#Consumers
from app.consumers.create_notification_consumer import consume_create_notification
from app.consumers.update_notification_consumer import consume_update_notification
from app.consumers.delete_notification_consumer import consume_delete_notification
from app.consumers.order_event_consumer import consume_create_order


# Async context manager for application lifespan events

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables for product-service-aimart....!!")
    
    # Create a task to run the Kafka consumer
    #consumer_task = asyncio.create_task(consume_messages())
    consumer_tasks = [
        asyncio.create_task(consume_create_notification()),
        asyncio.create_task(consume_update_notification()),
        asyncio.create_task(consume_delete_notification()),
        asyncio.create_task(consume_create_order()),
    ]
    
    # Create database tables
    create_db_and_tables()
    print("Database Tables Created in notification DB ....!!!")
    yield  # Application startup
        
    for task in consumer_tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass  # Handle cancellation if necessary
        finally:
             # Ensure the consumer is closed
            coro = task.get_coro()
            if coro and coro.cr_frame:
                consumer = coro.cr_frame.f_locals.get('consumer')
                if consumer:
                    await consumer.stop()


# Create FastAPI app with custom lifespan and metadata
app = FastAPI(
    lifespan=lifespan,
    title="MART_API_notification_service",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8010",
            "description": "Development Server"
        }
    ]
)

# Root endpoint
@app.get("/")
async def read_root():
    notification_count = count_all_notifications()
    return {"Welcome": "Welcome to the notification-service-aimart API", "Total Number of notifications in DB": notification_count}
# Endpoint to manage inventories


def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


@app.post("/notifications/", response_model=NotificationCreate)
async def create_new_notification(notification: NotificationCreate, session: Session = Depends(get_session)):
    notification_dict = notification.dict()
    notification_json = json.dumps(notification_dict, default=datetime_converter).encode("utf-8")
    await send_create_notification(notification_json)
    return notification

@app.get("/notifications/{notification_id}", response_model=Notification)
async def read_notification(notification_id: int, session: Session = Depends(get_session)):
    print("This is notification_id in main>>>>", notification_id)
    with session as session:
        notification_item = get_notification_by_id(session=session, notification_id=notification_id)
        print("After CRUD notification_item >>", notification_item)
        if not notification_item:
            raise HTTPException(status_code=404, detail="notification not found")
        else:
            print("Returning notification item:", notification_item.dict())
            return notification_item  # Explicitly convert to dict


@app.get("/notifications/", response_model=List[Notification])
async def read_notifications(session: Session = Depends(get_session)):
    with session as session:
        try:
            fetched_notifications = get_all_notifications(session)
            return fetched_notifications
        except Exception as e:
            print(f"Error in read_notifications: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.put("/notifications/{notification_id}", response_model=Notification)
async def update_existing_notification(notification_id: int, notification: NotificationUpdate, session: Session = Depends(get_session)):
    print(" create notification_id JSON >>>",notification_id)
    await send_update_notification(notification_id,notification)
    return Notification
   
@app.delete("/notifications/{notification_id}", response_model=Dict[str, str])
async def delete_existing_notification(notification_id: int, session: Session = Depends(get_session)):
    # notification = session.query(notification).filter(notification.id == notification_id).first()
    print("What is in notification_id in delet consumer >>>",notification_id)
    if not notification_id:
        raise HTTPException(status_code=404, detail="notification not found")
    
    await send_delete_notification(notification_id=notification_id) 
    return {str(notification_id): "deleted successfully"}