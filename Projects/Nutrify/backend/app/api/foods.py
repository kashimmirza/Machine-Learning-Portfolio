from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ..database import get_session
from ..models import FoodItem

router = APIRouter()

@router.post("/", response_model=FoodItem)
def create_food_item(food: FoodItem, session: Session = Depends(get_session)):
    session.add(food)
    session.commit()
    session.refresh(food)
    return food

@router.get("/", response_model=List[FoodItem])
def read_food_items(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    foods = session.exec(select(FoodItem).offset(skip).limit(limit)).all()
    return foods

@router.get("/{food_id}", response_model=FoodItem)
def read_food_item(food_id: int, session: Session = Depends(get_session)):
    food = session.get(FoodItem, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")
    return food
