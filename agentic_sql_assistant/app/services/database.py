from sqlmodel import SQLModel, Session, create_engine, select
from app.core.config import settings
from app.models.user import User
from app.models.session import Session as ChatSession
from typing import Generator

# Postgres Connection (App State)
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

class DatabaseService:
    def create_user(self, session: Session, user: User) -> User:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def get_user_by_email(self, session: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

db_service = DatabaseService()
