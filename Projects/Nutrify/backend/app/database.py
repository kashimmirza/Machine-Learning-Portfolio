from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nutrify_user:nutrify_password@localhost:5432/nutrify_db")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
