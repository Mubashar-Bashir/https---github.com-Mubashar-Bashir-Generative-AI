# app/crud/crud_inventory.py
from sqlmodel import Session, select
from app.models.inventory_model import Inventory
from app.db_c_e_t_session import get_session

def add_new_inventory(session: Session, inventory_data: dict):
    print("I am in CRUD Now Consumer Data ::+++>>>", inventory_data)
    with get_session() as session:
        inventory = Inventory(**inventory_data)
        session.add(inventory)
        session.commit()
        session.refresh(inventory)

def update_inventory(session: Session, inventory_id: int, update_data):
    print("I am in CRUD to Update >>>>---<<<<<<<<")
    print("Inventory to update is>>>> ", inventory_id, update_data)
    inventory = session.get(Inventory, inventory_id)
    print("I have searched to change inventory>>>", inventory)
    inventory_data = update_data
    print("ID removed from inventory_data to Up data>>>", inventory_data)
    if inventory_data:
        for key, value in inventory_data.items():
            print("Key =", key, "value = ", value, inventory_data)
            setattr(inventory, key, value)
        session.add(inventory)
        session.commit()
        session.refresh(inventory)
    return inventory

def delete_inventory_by_id(inventory_id: int, session: Session):
    print("I am in CRUD to delete>>>>>>>>>>>>>>>", inventory_id)
    inventory = get_inventory_by_id(inventory_id, session)
    if inventory:
        with session as session:
            session.delete(inventory)
            session.commit()
            return {"message": "Inventory Deleted Successfully from CRUD>>>>>>>>>"}
    return None

def get_inventory_by_id(inventory_id: int, session: Session):
    print("Inventory selected by id for get_inventory_by_id >>>>>>>>>>>>>>", inventory_id)
    with session as session:
        inventory = session.get(Inventory, inventory_id)
        return inventory


def get_all_inventory(session: Session):
    query = select(Inventory)
    result = session.exec(query)
    return result.fetchall()  # Fetch all results from the executed query