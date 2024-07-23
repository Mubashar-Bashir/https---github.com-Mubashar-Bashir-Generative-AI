
from typing import Annotated, List, Dict
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db_c_e_t_session import get_session, create_db_and_tables
import asyncio
from typing import AsyncGenerator
import json
from sqlmodel import SQLModel, Session,  select
# from app.consumers.add_product_consumer import consume_messages
from app.models.payment_model import Payment,PaymentUpdate
# app/main.py
from fastapi import FastAPI
from app.crud.crud_payment import get_all_payments,get_payment_by_id,create_payment,update_payment,delete_payment,count_all_payments
#from app.consumers.producer import send_create_product, send_update_product, send_delete_product
#Producers
from app.producers.create_payment_producer import send_create_payment
from app.producers.update_payment_producer import send_update_payment
from app.producers.delete_payment_producer import send_delete_payment
#Consumers
from app.consumers.create_payment_consumer import consume_create_payment
from app.consumers.update_payment_consumer import consume_update_payment
from app.consumers.delete_payment_consumer import consume_delete_payment


# Async context manager for application lifespan events

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables for payment-service-aimart....!!")
    
    # Create a task to run the Kafka consumer
    #consumer_task = asyncio.create_task(consume_messages())
    consumer_tasks = [
        asyncio.create_task(consume_create_payment()),
        asyncio.create_task(consume_update_payment()),
        asyncio.create_task(consume_delete_payment()),
    ]
    
    # Create database tables
    create_db_and_tables()
    print("Database Tables Created in payment DB ....!!!")
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
    title="MART_API_payment_service",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8008",
            "description": "Development Server"
        }
    ]
)

# Root endpoint
@app.get("/")
async def read_root():
    payment_count = count_all_payments()
    return {"Welcome": "Welcome to the payment-service-aimart API", "Total Number of payments in DB": payment_count}
# Endpoint to manage inventories
def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


# Create a new payment

@app.post("/payments/", response_model=Payment)
async def create_new_payment(payment: Payment, session: Session = Depends(get_session)):
    payment_dict = {field: getattr(payment, field) for field in payment.dict()}
    payment_json = json.dumps(payment_dict).encode("utf-8")
    print("payment JSON >>>",payment_json)
    # created_payment = create_payment(session=session,payment=payment)
    await send_create_payment(payment_json)
    return payment

@app.get("/payments/{payment_id}", response_model=Payment)
async def read_payment(payment_id: int, session: Session = Depends(get_session)):
    print("This is payment_id in main>>>>", payment_id)
    with session as session:
        payment_item = get_payment_by_id(session=session, payment_id=payment_id)
        print("After CRUD payment_item >>", payment_item)
        if not payment_item:
            raise HTTPException(status_code=404, detail="payment not found")
        else:
            print("Returning payment item:", payment_item.dict())
            return payment_item  # Explicitly convert to dict


@app.get("/payments/", response_model=list[Payment])
async def read_payments(session: Session = Depends(get_session)):
    with session as session:
        try:
            fetched_payments = get_all_payments(session)
            return fetched_payments
        except Exception as e:
            print(f"Error in read_payments: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@app.put("/payments/{payment_id}", response_model=Payment)
async def update_existing_payment(payment_id: int, payment: PaymentUpdate, session: Session = Depends(get_session)):
    print(" create payment_id JSON >>>",payment_id)
    await send_update_payment(payment_id,payment)
    return payment
# @app.put("/payments/{payment_id}", response_model=Payment)
# async def update_existing_payment(payment_id: int, payment_update: PaymentUpdate, session: Session = Depends(get_session)):
#     print(" create payment_id JSON >>>", payment_id)
#     payment = update_payment(session, payment_id, payment_update)
#     if not payment:
#         raise HTTPException(status_code=404, detail="Payment not found")
    
#     await send_update_payment(payment_id, payment_update)
#     return payment   

@app.delete("/payments/{payment_id}", response_model=dict[str, str])
async def delete_existing_payment(payment_id: int, session: Session = Depends(get_session)):
    # payment = session.query(payment).filter(payment.id == payment_id).first()
    print("What is in payment_id in delet consumer >>>",payment_id)
    if not payment_id:
        raise HTTPException(status_code=404, detail="payment not found")
    
    await send_delete_payment(payment_id=payment_id) 
    return {str(payment_id): "deleted successfully"}