
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db_c_e_t_session import create_db_and_tables, get_session
import asyncio
from typing import AsyncGenerator
import json
import uuid

from sqlmodel import SQLModel, Session,  select
# from app.consumers.add_product_consumer import consume_messages
from app.models.product_model import Product, ProductUpdate, ProductCreate
# app/main.py
from fastapi import FastAPI
from app.crud.crud_product import get_by_id,delete_product_by_id, get_all_products
#from app.consumers.producer import send_create_product, send_update_product, send_delete_product
#Producers
from app.producers.create_product_producer import send_create_product
from app.producers.update_product_producer import send_update_product
from app.producers.delete_product_producer import send_delete_product
#Consumers
from app.consumers.create_product_consumer import consume_create_product
from app.consumers.update_product_consumer import consume_update_product
from app.consumers.delete_product_consumer import consume_delete_product


# Async context manager for application lifespan events

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables for product-service-aimart..!!")
    
    # Create a task to run the Kafka consumer
    #consumer_task = asyncio.create_task(consume_messages())
    consumer_tasks = [
        asyncio.create_task(consume_create_product()),
        asyncio.create_task(consume_update_product()),
        asyncio.create_task(consume_delete_product()),
    ]
    
    # Create database tables
    create_db_and_tables()
    print("Database Tables Created in Product-DB ...!!!")
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
    title="MART_API_Product_service",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8007",
            "description": "Development Server"
        }
    ]
)


# Root endpoint
@app.get("/")
async def read_root():
    return {"Welcome": "welcome to my mobi product-service-aimart"}

# Define your endpoint to manage products
# @app.post("/manage-products", response_model=Product)
# async def create_product(product: Product, session: Session = Depends(get_session)):
#     product_dict = {field: getattr(product, field) for field in product.dict()}
#     product_json = json.dumps(product_dict).encode("utf-8")
#     print("product_JSON_main>>>>>>:", product_json)
#     # Produce messag
#     await send_create_product(product_json)
#     return product

@app.post("/manage-products", response_model=Product)
async def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    # Create a new Product instance with a generated UUID
    # product = Product(**product_create.dict())
     
    # session.add(product)
    # session.commit()
    # session.refresh(product)
    
    # return product    
    product_dict = {field: getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("product_JSON_main>>>>>>:", product_json)
    # Produce messag
    await send_create_product(product_json)
    return product

# # Read All Products
@app.get("/manage-products/all", response_model = List[Product])
def read_products(session: Annotated[Session, Depends(get_session)]):
    #all_products =  get_all_products(session)
    with session as session:
        # all_products = session.exec(select(Product)).all()
        all_products = get_all_products(session = session)
        return all_products


@app.get("/manage-products/{product_id}", response_model=Product)
async def get_single_product(product_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]) -> Product:
    """ Get a single product by ID"""
    product = get_by_id(product_id=product_id, session=session)
    if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

# Delete a product by ID
@app.delete("/manage-products/{product_id}", response_model=dict)
async def delete_single_product(product_id: uuid.UUID, session: Annotated[Session, Depends(get_session)]):
    """ Delete a single product by ID"""
    #product_json = json.dumps(product_id).encode("utf-8")
   
    try:
        
        await send_delete_product(product_id=product_id)
        return {"message": f"Delete request for product ID {str(product_id)} sent."}
    except HTTPException as e:
        print(f"HTTP Exception: {e}")
        raise e
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


    
@app.patch("/manage-products/{product_id}", response_model=Product)
async def update_single_product(product_id: uuid.UUID, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
    """ Update a single product by ID"""
    await send_update_product(product_id=product_id, to_update_product_data=product)
    return {**product.dict(), "id": str(product_id)}
