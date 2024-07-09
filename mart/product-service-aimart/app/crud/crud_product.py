# app/consumers/add_product_consumer.py
from aiokafka import AIOKafkaConsumer
import json
from fastapi import HTTPException
from app.db_c_e_t_session import get_session
from app.models.product_model import Product
from sqlmodel import select
from app.consumers.config import KAFKA_BROKER_URL, ADD_PRODUCT_TOPIC, UPDATE_PRODUCT_TOPIC, DELETE_PRODUCT_TOPIC
from sqlmodel import Session
from app.models.product_model import Product

def add_new_product(session: Session, product_data: dict):
    print("iam in CRUD Now Consumer Data ::+++>>>",product_data)
    with (get_session()) as session:
            product = Product(**product_data)
            session.add(product)
            session.commit()
            session.refresh(product)

def update_product(session: Session, product_id: int, update_data):
    print("i am in CRUD to Update >>>>---<<<<<<<<")
    print("Product to update is>>>> ",product_id,update_data)
    product = session.get(Product, product_id)
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

def delete_product_by_id(product_id: int, session: Session):
    # print("I am in Crud to delete>>>>>>>>>>>>>>>", product_id)
    product = get_by_id(product_id, session)
    if product:
        with session as session:
            session.delete(product)
            session.commit()
            return {"message": "Product Deleted Successfully from CRUD>>>>>>>>>"}
    return None
    
# get_by_id
def get_by_id( product_id: int, session: Session):
    print("product selected by id for get_by_id >>>>>>>>>>>>>>", product_id)
    with session as session:  
        product = session.get(Product, product_id)
        return product

# Get All Products from the Database
def get_all_products(session: Session):
    all_products = session.exec(select(Product)).all()
    return all_products