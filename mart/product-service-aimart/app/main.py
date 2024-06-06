from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db_c_e_t_session import create_db_and_tables,get_session
import asyncio
from sqlmodel import Session, SQLModel

from app.models.product_model import Product, ProductUpdate
from app.crud.crud_product import add_new_product, get_all_products, get_product_by_id, delete_product_by_id, update_product_by_id

# Async context manager for application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables for product-service-aimart..")
    create_db_and_tables()  # Create database tables
    yield  # Application startup

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
    return {"Welcome": "welcome to my mobi product-service-aimart local computer"}

# Create a product
@app.post("/products", response_model=Product)
async def create_new_product(product: Product, session: Annotated[Session, Depends(get_session)]):
    new_product = add_new_product(product, session)
    return new_product

@app.get("/products", response_model = List[Product])
async def get_products(session=get_session()):
    all_products = get_all_products(session)
    return all_products