from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from back  import crud
from back import schemas
from back import models

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    return crud.get_task(db, task_id)

@router.post("/")
def create_task(meeting_id: int, content: str, db: Session = Depends(get_db)):
    return crud.create_task(db, meeting_id, content)

