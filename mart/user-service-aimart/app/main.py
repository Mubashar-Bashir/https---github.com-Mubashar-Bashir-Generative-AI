#MAIN.PY
from typing import Annotated, List
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.db_c_e_t_session import create_db_and_tables, get_session
import asyncio
from typing import AsyncGenerator
import json

from sqlmodel import SQLModel, Session,  select
# from app.consumers.add_user_consumer import consume_messages
from app.models.user_model import User,UserUpdate
# app/main.py
from fastapi import FastAPI
from app.crud.crud_user import create_user,get_user_by_id,get_all_users,update_user,delete_user_by_id,count_all_users
#from app.consumers.producer import send_create_user, send_update_user, send_delete_user
#Producers
from app.producers.create_user_producer import send_create_user
from app.producers.update_user_producer import send_update_user
from app.producers.delete_user_producer import send_delete_user
#Consumers
from app.consumers.create_user_consumer import consume_create_user
from app.consumers.update_user_consumer import consume_update_user
from app.consumers.delete_user_consumer import consume_delete_user


# Async context manager for application lifespan events

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables for user-service-aimart....!!")
    
    # Create a task to run the Kafka consumer
    #consumer_task = asyncio.create_task(consume_messages())
    consumer_tasks = [
        asyncio.create_task(consume_create_user()),
        asyncio.create_task(consume_update_user()),
        asyncio.create_task(consume_delete_user()),
    ]
    
    # Create database tables
    create_db_and_tables()
    print("Database Tables Created in user-DB ..!!!")
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
    title="MART_API_user_service",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8006",
            "description": "Development Server"
        }
    ]
)


# Root endpoint
@app.get("/")
async def read_root():
    user_count = count_all_users()
    return {"Welcome": "welcome to my mobi user-service-aimart","Total Number of users Count>>":user_count}

# Define your endpoint to manage users
@app.post("/manage-users", response_model=User)
async def create_user(user: User, session: Session = Depends(get_session)):
    user_dict = {field: getattr(user, field) for field in user.dict()}
    user_json = json.dumps(user_dict).encode("utf-8")
    print("user_JSON_main>>>>>>:", user_json)
    # Produce messag
    await send_create_user(user_json)
    return user
    

# # Read All users
@app.get("/manage-users/all", response_model = List[User])
def read_users(session: Annotated[Session, Depends(get_session)]):
    #all_users =  get_all_users(session)
    with session as session:
        # all_users = session.exec(select(user)).all()
        all_users = get_all_users(session = session)
        return all_users


@app.get("/manage-users/{user_id}", response_model=User)
async def get_single_user(user_id: int, session: Annotated[Session, Depends(get_session)]) -> User:
    """ Get a single user by ID"""
    with session as session:
        user = get_user_by_id(user_id=user_id, session=session)
        if not user:
                raise HTTPException(status_code=404, detail="user not found")
        return user

# Delete a user by ID
@app.delete("/manage-users/{user_id}", response_model=dict)
async def delete_single_user(user_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Delete a single user by ID"""
    #user_json = json.dumps(user_id).encode("utf-8")
   
    try:
        
        await send_delete_user(user_id=user_id)
        return {"message": f"user ID {user_id} Deleted !!!"}
    except HTTPException as e:
        print(f"HTTP Exception: {e}")
        raise e
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


    
@app.put("/manage-users/{user_id}", response_model=User)
async def update_single_user(user_id: int, user: UserUpdate, session: Annotated[Session, Depends(get_session)]):
    """ Update a single user by ID"""
    await send_update_user(user_id=user_id, to_update_user_data = user)
    return user
