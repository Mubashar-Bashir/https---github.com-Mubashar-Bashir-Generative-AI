from typing import Generator
from app import order_settings
from sqlmodel import Session, SQLModel, create_engine


from contextlib import contextmanager
# Kafka Producer as a dependency



connection_string = str(order_settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)



@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
        session.commit()  # Commit changes if no exceptions occur
    except Exception as e:
        session.rollback()  # Rollback changes if an exception occurs
        raise
    finally:
        session.close()
# @contextmanager
# def get_session():
#     with Session(engine) as session:
#         yield session
# @asynccontextmanager
# async def get_session():
#     async with SessionLocal() as session:
#         yield session