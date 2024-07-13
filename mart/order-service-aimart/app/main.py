
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db_c_e_t_session import get_session, create_db_and_tables
import asyncio
from typing import AsyncGenerator
from sqlmodel import SQLModel, Session,  select
# from app.consumers.add_product_consumer import consume_messages
from app.models.order_model import Order,OrderUpdate
# app/main.py
from fastapi import FastAPI
from app.crud.crud_order import get_all_orders,get_order,create_order,update_order,delete_order
#from app.consumers.producer import send_create_product, send_update_product, send_delete_product
#Producers
from app.producers.create_order_producer import send_create_order
from app.producers.update_order_producer import send_update_order
from app.producers.delete_order_producer import send_delete_order
#Consumers
from app.consumers.create_order_consumer import consume_create_order
from app.consumers.update_order_consumer import consume_update_order
from app.consumers.delete_order_consumer import consume_delete_order


# Async context manager for application lifespan events

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables for product-service-aimart....!!")
    
    # Create a task to run the Kafka consumer
    #consumer_task = asyncio.create_task(consume_messages())
    consumer_tasks = [
        asyncio.create_task(consume_create_order()),
        asyncio.create_task(consume_update_order()),
        asyncio.create_task(consume_delete_order()),
    ]
    
    # Create database tables
    create_db_and_tables()
    print("Database Tables Created in order DB ....!!!")
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
    title="MART_API_order_service",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8009",
            "description": "Development Server"
        }
    ]
)

# Root endpoint
@app.get("/")
async def read_root():
    return {"Welcome": "Welcome to the order-service-aimart API"}

# Endpoint to manage inventories

# Create a new order

@app.post("/orders/", response_model=Order)
def create_new_order(order: Order, session: Session = Depends(get_session)):
    return create_order(session, order)

@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int, session: Session = Depends(get_session)):
    order = get_order(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders/", response_model=List[Order])
def read_orders(session: Session = Depends(get_session)):
    return get_all_orders(session)

@app.put("/orders/{order_id}", response_model=Order)
def update_existing_order(order_id: int, order_update: OrderUpdate, session: Session = Depends(get_session)):
    updated_order = update_order(session, order_id, order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@app.delete("/orders/{order_id}", response_model=bool)
def delete_existing_order(order_id: int, session: Session = Depends(get_session)):
    success = delete_order(session, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return success