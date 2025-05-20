from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from back.crud import meetings as crud

router = APIRouter(prefix="/meetings", tags=["Meetings"])

@router.get("/{meeting_id}")
def read_meeting(meeting_id: int, db: Session = Depends(get_db)):
    return crud.get_meeting(db, meeting_id)

@router.post("/")
def create_meeting(title: str, db: Session = Depends(get_db)):
    return crud.create_meeting(db, title)

