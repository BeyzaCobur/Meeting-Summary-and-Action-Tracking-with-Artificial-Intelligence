from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from back.database import get_db
from back import crud, schemas
from typing import List

router = APIRouter(prefix="/transcripts", tags=["Transcripts"])

@router.get("/", response_model=List[schemas.Transcript])
def get_transcripts(db: Session = Depends(get_db)):
    return crud.get_transcripts(db)
