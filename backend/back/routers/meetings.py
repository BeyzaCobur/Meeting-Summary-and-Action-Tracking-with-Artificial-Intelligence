from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from back import schemas
from back import crud

router = APIRouter(prefix="/meetings", tags=["Meetings"])

@router.get("/{meeting_id}", response_model=schemas.Meeting)
def read_meeting(meeting_id: UUID, db: Session = Depends(get_db)):
    return crud.get_meeting(db, meeting_id)



@router.post("/", response_model=schemas.Meeting)
def create_meeting(meeting: schemas.MeetingCreate, db: Session = Depends(get_db)):
    return crud.create_meeting(db, meeting)
