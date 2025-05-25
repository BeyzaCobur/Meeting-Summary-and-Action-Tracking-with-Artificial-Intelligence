from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from back import crud

router = APIRouter(prefix="/transcripts", tags=["Transcripts"])

@router.get("/{transcript_id}")
def read_transcript(transcript_id: int, db: Session = Depends(get_db)):
    return crud.get_transcript(db, transcript_id)

@router.post("/transcribe")
def create_transcript(meeting_id: int, content: str, db: Session = Depends(get_db)):
    return crud.create_transcript(db, meeting_id, content)

