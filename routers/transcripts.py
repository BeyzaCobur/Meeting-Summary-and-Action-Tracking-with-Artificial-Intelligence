from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from back.crud import transcripts as crud

router = APIRouter(prefix="/transcripts", tags=["Transcripts"])

@router.get("/{transcript_id}")
def read_transcript(transcript_id: int, db: Session = Depends(get_db)):
    return crud.get_transcript(db, transcript_id)

@router.post("/")
def create_transcript(meeting_id: int, content: str, db: Session = Depends(get_db)):
    return crud.create_transcript(db, meeting_id, content)

