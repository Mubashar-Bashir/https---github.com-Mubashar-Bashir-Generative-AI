
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db_c_e_t_session import create_db_and_tables, get_session
import asyncio
from typing import AsyncGenerator
import json

from sqlmodel import SQLModel, Session,  select
# from app.consumers.add_product_consumer import consume_messages
from app.models.inventory_model import Inventory, InventoryUpdate
# app/main.py
from fastapi import FastAPI
from app.crud.crud_inventory import get_all_inventory,get_inventory_by_id,delete_inventory_by_id,update_inventory
#from app.consumers.producer import send_create_product, send_update_product, send_delete_product
#Producers
from app.producers.create_inventory_producer import send_create_inventory
from app.producers.update_inventory_producer import send_update_inventory
from app.producers.delete_inventory_producer import send_delete_inventory
#Consumers
from app.consumers.create_inventory_consumer import consume_create_inventory
from app.consumers.update_inventory_consumer import consume_update_inventory
from app.consumers.delete_inventory_consumer import consume_delete_inventory


# Async context manager for application lifespan events

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables for product-service-aimart....!!")
    
    # Create a task to run the Kafka consumer
    #consumer_task = asyncio.create_task(consume_messages())
    consumer_tasks = [
        asyncio.create_task(consume_create_inventory()),
        asyncio.create_task(consume_update_inventory()),
        asyncio.create_task(consume_delete_inventory()),
    ]
    
    # Create database tables
    create_db_and_tables()
    print("Database Tables Created in Inventory DB .....!!!")
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
    title="MART_API_Inventory_service",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8011",
            "description": "Development Server"
        }
    ]
)

# Root endpoint
@app.get("/")
async def read_root():
    return {"Welcome": "Welcome to the inventory-service-aimart API"}

# Endpoint to manage inventories

# Create a new inventory
@app.post("/manage-inventories", response_model=Inventory)
async def create_inventory(inventory: Inventory, session: Session = Depends(get_session)):
    inventory_dict = {field: getattr(inventory, field) for field in inventory.dict()}
    inventory_json = json.dumps(inventory_dict).encode("utf-8")
    print("Inventory JSON:", inventory_json)
    await send_create_inventory(inventory_json)
    return inventory

# Read all inventories
@app.get("/manage-inventories/all", response_model=list[Inventory])
async def read_inventories(session: Session = Depends(get_session)):
    with session as session:
        try:
            fetched_inventories = get_all_inventory(session)
            return fetched_inventories
        except Exception as e:
            print(f"Error in read_inventories: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# Read a single inventory by ID            need to check and verify
@app.get("/manage-inventories/{inventory_id}", response_model=Inventory)
async def read_inventory(inventory_id: int, session: Session = Depends(get_session)):
    print("This is inventoy_id in main>>>>",inventory_id)
    with session as session:
        inventory_item = get_inventory_by_id(session=session, inventory_id=inventory_id)
        print("After CRUD Inventory_item ",inventory_item)
        if not inventory_item:
            raise HTTPException(status_code=404, detail="Inventory not found")
        else:
            print("Returning inventory item:", inventory_item.dict())
            return inventory_item.dict()  # Explicitly convert to dict
    
# Update an existing inventory
@app.put("/manage-inventories/{inventory_id}", response_model=Inventory)
async def update_inventory(inventory_id: int, inventory: InventoryUpdate, session: Session = Depends(get_session)):
    await send_update_inventory(inventory_id, inventory)
    return inventory

# Delete an inventory
@app.delete("/manage-inventories/{inventory_id}", response_model=dict)
async def delete_inventory(inventory_id: int, session: Session = Depends(get_session)):
    await send_delete_inventory(inventory_id)
    #return {"message": f"Delete request for inventory ID {inventory_id} sent."}