from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from api.db import models, database
from api import models as schemas
from src.awesome_agent_api.infrastructure.web3_service import Web3Service

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Awesome Agent API",
    description="API for AgentPay with MNEE integration",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

web3_service = Web3Service()

@app.get("/")
async def root():
    return {"message": "Welcome to Awesome Agent API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.wallet_address == user.wallet_address).first()
    if db_user:
        return db_user
    db_user = models.User(wallet_address=user.wallet_address, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        description=task.description, 
        price_mnee=task.price_mnee,
        creator_id=task.creator_id,
        scheduled_at=task.scheduled_at
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/tasks/{task_id}/complete", response_model=schemas.Task)
def complete_task(task_id: int, update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.status = models.TaskStatus.COMPLETED.value
    if update.result_data:
        db_task.result_data = update.result_data
    if update.worker_id:
        db_task.worker_id = update.worker_id
        
    db.commit()
    db.refresh(db_task)
    return db_task

@app.post("/tasks/{task_id}/validate", response_model=schemas.Task)
def validate_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    db_task.status = models.TaskStatus.VALIDATED.value
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/scheduled", response_model=List[schemas.Task])
def get_scheduled_tasks(db: Session = Depends(get_db)):
    # In a real app, we would filter by scheduled_at <= now
    return db.query(models.Task).filter(models.Task.scheduled_at != None).all()

@app.post("/content", response_model=schemas.Content)
def create_content(content: schemas.ContentCreate, db: Session = Depends(get_db)):
    db_content = models.Content(
        creator_id=content.creator_id,
        title=content.title,
        price_mnee=content.price_mnee,
        content_data=content.content_data
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@app.get("/content/{content_id}", response_model=schemas.Content)
def read_content(content_id: int, user_id: int, db: Session = Depends(get_db)):
    db_content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Check access
    if db_content.creator_id != user_id:
        access = db.query(models.Access).filter(
            models.Access.content_id == content_id,
            models.Access.user_id == user_id
        ).first()
        if not access:
            raise HTTPException(status_code=403, detail="Access denied. Payment required.")
            
    return db_content

@app.post("/payments/verify")
def verify_payment(payment: schemas.PaymentVerify, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == payment.task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if payment already exists
    existing_payment = db.query(models.Payment).filter(models.Payment.transaction_hash == payment.transaction_hash).first()
    if existing_payment:
        return {"status": "already_processed", "verified": existing_payment.verified == 1}

    # Verify on-chain
    # In a real app, we should probably do this asynchronously or have a separate worker
    # But for the prototype, we'll do it synchronously
    is_valid = web3_service.verify_transaction(
        payment.transaction_hash, 
        db_task.price_mnee, 
        "0xRecipientAddress" # TODO: This should be the agent's or platform's wallet address
    )

    verification_status = 1 if is_valid else 2
    
    db_payment = models.Payment(
        task_id=payment.task_id,
        transaction_hash=payment.transaction_hash,
        amount=db_task.price_mnee, # Assuming full payment
        sender_address=payment.sender_address,
        verified=verification_status
    )
    db.add(db_payment)
    
    if is_valid:
        db_task.status = models.TaskStatus.IN_PROGRESS.value
        # Trigger Agent Logic here (e.g. LangChain)
        # For now, just mark as in progress
    
    db.commit()
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid payment transaction")

    return {"status": "verified", "task_status": db_task.status}
