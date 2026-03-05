from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "Login not implemented yet"}

@router.post("/signup")
def signup():
    return {"message": "Signup not implemented yet"}
