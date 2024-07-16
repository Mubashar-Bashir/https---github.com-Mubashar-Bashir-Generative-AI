
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from app.db_c_e_t_session import create_db_and_tables, get_session
import asyncio
from typing import AsyncGenerator


from sqlmodel import SQLModel, Session,  select
from app.consumers.add_product_consumer import consume_messages
from app.models.product_model import Product, ProductUpdate
# app/main.py
from fastapi import FastAPI
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
    print("Creating tables for product-service-aimart....")
    
    # Create a task to run the Kafka consumer
   # consumer_task = asyncio.create_task(consume_messages())
    consumer_tasks = [
        asyncio.create_task(consume_create_product()),
        asyncio.create_task(consume_update_product()),
        asyncio.create_task(consume_delete_product())
    ]
    
    # Create database tables
    create_db_and_tables()
    print("Database Tables Created....!!!")
    yield  # Application startup
    
    # Teardown logic if needed
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

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
def read_root():
    return {"Welcome": "welcome to my mobi product-service-aimart"}

# Define your endpoint to manage products
@app.post("/manage-products", response_model=Product)
async def create_product(product: Product, session: Session = Depends(get_session)):
    await send_create_product(product.dict())
    return product
    

# # Read All Products
# @app.get("/manage-products/all", response_model = List[Product])
# async def read_products(session: Annotated[Session, Depends(get_session)]):
#     #all_products =  get_all_products(session)
#     all_products = session.exec(select(Product)).all()
#     return all_products

# Get All Products from the Database
def get_all_products(session: Session):
    all_products = session.exec(select(Product)).all()
    return all_products

@app.get("/manage-products/{product_id}", response_model=Product)
async def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Get a single product by ID"""
    product = session.get(Product, product_id)
    if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/manage-products/{product_id}", response_model=dict)
async def delete_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):     
    """ Delete a single product by ID"""
    await send_delete_product(product_id)
    return {"message": "Product deletion request received"}

    
@app.patch("/manage-products/{product_id}", response_model=Product)
async def update_single_product(product_id: int, product: ProductUpdate, session: Annotated[Session, Depends(get_session)]):
    """ Update a single product by ID"""
    product_data = ProductUpdate.dict()
    product_data['id'] = product_id
    await send_update_product(product_data)
    return product_data