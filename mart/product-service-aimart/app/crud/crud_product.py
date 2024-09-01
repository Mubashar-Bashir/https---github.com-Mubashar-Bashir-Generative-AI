# app/consumers/add_product_consumer.py
from aiokafka import AIOKafkaConsumer
import json
from fastapi import HTTPException
from app.db_c_e_t_session import get_session
from app.models.product_model import Product
from sqlmodel import select
from sqlmodel import Session
from app.models.product_model import Product
from uuid import uuid4
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func  # Import func from sqlalchemy.sql

def add_new_product(session: Session, product_data: dict):
    print("iam in CRUD Now Consumer Data ::+++>>>",product_data)
    
    try:
         # Generate a new UUID if 'id' is not provided
        if 'id' not in product_data:
            product_data['id'] = str(uuid4())

        with (get_session()) as session:
                product = Product(**product_data)
                session.add(product)
                session.commit()
                session.refresh(product)
                print(f"Product with ID {product.id} created successfully.")
                return product
    except IntegrityError as e: 
        # Handle specific integrity errors, such as unique constraint violations
        session.rollback()  # Rollback the transaction
        print(f"Error while adding new product: {e}")
        raise HTTPException(status_code=400, detail="Product already exists or other integrity error")
    
    except Exception as e:
        # Handle general exceptions
        print(f"Error while adding new product: {e}")
        raise

def update_product(session: Session, product_id: uuid.UUID, update_data):
    print("i am in CRUD to Update >>>>---<<<<<<<<")
    print("Product to update is>>>> ",str(product_id),update_data)
    product = session.get(Product, str(product_id))
    print("I have searched to change product>>>",product)
    product_data = update_data
    print("ID removed from product_data to Up data>>>",product_data)
    if product_data:
        for key, value in product_data.items():
            print("Key =",key,"value = ",value,product_data)
            setattr(product, key, value)
        session.add(product)
        session.commit()
        session.refresh(product)
    return product

def delete_product_by_id(product_id: uuid.UUID, session: Session):
    # print("I am in Crud to delete>>>>>>>>>>>>>>>", product_id)
    product = get_by_id(product_id, session)
    if product:
        with session as session:
            session.delete(product)
            session.commit()
            return {"message": "Product Deleted Successfully from CRUD>>>>>>>>>"}
    return None
    
# get_by_id
def get_by_id( product_id: uuid.UUID, session: Session):
    print("product selected by id for get_by_id >>>>>>>>>>>>>>", str(product_id))
    with session as session:  
        product = session.get(Product, product_id)
        return product

# Get All Products from the Database
def get_all_products(session: Session):
    all_products = session.exec(select(Product)).all()
    return all_products

def count_all_Products() -> int:
    with get_session() as session:
        # Use select to count all Product entries
        count_query = select(func.count(Product.id))
        result = session.exec(count_query).one()
        return result
