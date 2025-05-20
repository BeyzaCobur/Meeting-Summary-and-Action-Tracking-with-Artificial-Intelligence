from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from back.crud import users as crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

@router.post("/")
def create_user(name: str, db: Session = Depends(get_db)):
    return crud.create_user(db, name)

