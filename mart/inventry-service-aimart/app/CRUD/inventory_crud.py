from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItem

def add_new_inventory_item(inventory_item_data: InventoryItem, session: Session):
    try:
        session.add(inventory_item_data)
        session.commit()
        session.refresh(inventory_item_data)
        return inventory_item_data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add inventory item: {str(e)}")

def get_all_inventory_items(session: Session):
    try:
        return session.exec(select(InventoryItem)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve inventory items: {str(e)}")

def get_inventory_item_by_id(inventory_item_id: int, session: Session):
    try:
        inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
        if inventory_item is None:
            raise HTTPException(status_code=404, detail="Inventory Item not found")
        return inventory_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve inventory item: {str(e)}")


def delete_inventory_item_by_id(inventory_item_id: int, session: Session):
    try:
        inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
        if inventory_item is None:
            raise HTTPException(status_code=404, detail="Inventory Item not found")
        session.delete(inventory_item)
        session.commit()
        return {"message": "Inventory Item Deleted Successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete inventory item: {str(e)}")
