# app/crud/crud_inventory.py
from fastapi import HTTPException
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

# Define the function to get an inventory by ID using plain SQLModel queries
def get_inventory_by_id(inventory_id: int, session: Session) -> Inventory:
    ##############################
    print("I am in CRUD to get-inventroy by id >>>>>>>>>>>>>>>", inventory_id)
    # inventory = get_inventory_by_id(inventory_id, session)
    # print("inventory_id get through session = ",inventory)
    # query = select(Inventory).where(Inventory.id == inventory_id)
    # print("Query >>>>>",query.all())
    # result = session.exec(query).first()
    # print("Result >>>>> ",result.all())
    # if result is None:
    #     raise HTTPException(status_code=404, detail="Inventory not found")
    # return result
    ##############################
    # with session as session:``
    #     query = select(Inventory).where(Inventory.id == inventory_id)
    #     print("Query >>>>>",query.all())
    #     result = session.exec(query).first()
    #     print("Result >>>>> ",result.all())
    #     if result is None:
    #         raise HTTPException(status_code=404, detail="Inventory not found")
    #     return result


def get_all_inventory(session: Session):
    try:
        query = select(Inventory)
        result = session.execute(query)
        return result.fetchall()  # Fetch all results from the executed query
    except Exception as e:
        print(f"Error fetching inventory: {e}")
        raise