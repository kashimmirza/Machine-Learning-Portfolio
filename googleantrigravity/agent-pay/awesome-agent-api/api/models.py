from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    REQUESTER = "requester"
    WORKER = "worker"
    CREATOR = "creator"

class UserBase(BaseModel):
    wallet_address: str
    role: UserRole = UserRole.REQUESTER

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    description: str
    price_mnee: float
    scheduled_at: Optional[datetime] = None

class TaskCreate(TaskBase):
    creator_id: int # In a real app, this would be inferred from auth

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    result_data: Optional[str] = None
    worker_id: Optional[int] = None

class Task(TaskBase):
    id: int
    status: str
    created_at: datetime
    agent_id: Optional[str] = None
    creator_id: Optional[int] = None
    worker_id: Optional[int] = None
    result_data: Optional[str] = None

    class Config:
        from_attributes = True

class PaymentVerify(BaseModel):
    task_id: int
    transaction_hash: str
    sender_address: str

class ContentBase(BaseModel):
    title: str
    price_mnee: float
    content_data: str

class ContentCreate(ContentBase):
    creator_id: int

class Content(ContentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

