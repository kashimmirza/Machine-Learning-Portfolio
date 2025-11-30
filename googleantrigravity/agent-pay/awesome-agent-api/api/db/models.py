from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATED = "validated"

class UserRole(str, enum.Enum):
    REQUESTER = "requester"
    WORKER = "worker"
    CREATOR = "creator"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, unique=True, index=True)
    role = Column(String, default=UserRole.REQUESTER.value)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks_created = relationship("Task", foreign_keys="[Task.creator_id]", back_populates="creator")
    tasks_worked = relationship("Task", foreign_keys="[Task.worker_id]", back_populates="worker")
    content_created = relationship("Content", back_populates="creator")
    access_rights = relationship("Access", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    status = Column(String, default=TaskStatus.PENDING.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    price_mnee = Column(Float, nullable=False)
    
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Nullable for backward compatibility/anonymous
    worker_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    agent_id = Column(String, nullable=True) # ID of the agent assigned (if external)
    
    scheduled_at = Column(DateTime, nullable=True)
    result_data = Column(Text, nullable=True)

    creator = relationship("User", foreign_keys=[creator_id], back_populates="tasks_created")
    worker = relationship("User", foreign_keys=[worker_id], back_populates="tasks_worked")
    payments = relationship("Payment", back_populates="task")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    transaction_hash = Column(String, unique=True, index=True)
    amount = Column(Float)
    sender_address = Column(String)
    verified = Column(Integer, default=0) # 0: pending, 1: verified, 2: failed
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="payments")

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    price_mnee = Column(Float)
    content_data = Column(Text) # URL or text content
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User", back_populates="content_created")
    access_grants = relationship("Access", back_populates="content")

class Access(Base):
    __tablename__ = "access"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("content.id"))
    granted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="access_rights")
    content = relationship("Content", back_populates="access_grants")
