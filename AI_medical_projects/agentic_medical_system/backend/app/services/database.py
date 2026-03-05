from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.core.config import settings
from app.models.user import User
from app.models.session import Session as ChatSession

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        connection_url = (
            f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )
        
        self.engine = create_engine(
            connection_url,
            pool_pre_ping=True,
            poolclass=QueuePool,
            pool_size=settings.POSTGRES_POOL_SIZE,
            max_overflow=settings.POSTGRES_MAX_OVERFLOW,
            pool_timeout=30,
            pool_recycle=1800,
        )
        
        # Create tables (simple code-first migration for this demo)
        # In real prod, use Alembic
        try:
            SQLModel.metadata.create_all(self.engine)
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")

    async def health_check(self) -> bool:
        try:
            with Session(self.engine) as session:
                session.exec(select(1))
            return True
        except Exception:
            return False

    # --- User Operations ---
    async def create_user(self, email: str, password_hash: str) -> User:
        with Session(self.engine) as session:
            user = User(email=email, hashed_password=password_hash)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        with Session(self.engine) as session:
            statement = select(User).where(User.email == email)
            return session.exec(statement).first()

    async def get_user(self, user_id: int) -> Optional[User]:
        with Session(self.engine) as session:
            return session.get(User, user_id)

    # --- Session Operations ---
    async def create_session(self, session_id: str, user_id: int, name: str = "") -> ChatSession:
        with Session(self.engine) as session:
            chat_session = ChatSession(id=session_id, user_id=user_id, name=name)
            session.add(chat_session)
            session.commit()
            session.refresh(chat_session)
            return chat_session

    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        with Session(self.engine) as session:
            return session.get(ChatSession, session_id)

    async def get_user_sessions(self, user_id: int) -> List[ChatSession]:
        with Session(self.engine) as session:
            statement = select(ChatSession).where(ChatSession.user_id == user_id)
            return session.exec(statement).all()

database_service = DatabaseService()
