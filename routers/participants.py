from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from back.crud import participants as crud

router = APIRouter(prefix="/participants", tags=["Participants"])

@router.get("/{participant_id}")
def read_participant(participant_id: int, db: Session = Depends(get_db)):
    return crud.get_participant(db, participant_id)

@router.post("/")
def create_participant(name: str, meeting_id: int, db: Session = Depends(get_db)):
    return crud.create_participant(db, name, meeting_id)

