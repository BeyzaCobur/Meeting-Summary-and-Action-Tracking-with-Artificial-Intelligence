from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from back import crud
from back import schemas

router = APIRouter(prefix="/summaries", tags=["Summaries"])

@router.get("/{summary_id}")
def read_summary(summary_id: int, db: Session = Depends(get_db)):
    return crud.get_summary(db, summary_id)

@router.post("/")
def create_summary(meeting_id: int, content: str, db: Session = Depends(get_db)):
    return crud.create_summary(db, meeting_id, content)

