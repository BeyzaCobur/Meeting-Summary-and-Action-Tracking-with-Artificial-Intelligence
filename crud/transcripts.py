from sqlalchemy.orm import Session
from back.models import Transcript

def get_transcript(db: Session, transcript_id: int):
    return db.query(Transcript).filter(Transcript.id == transcript_id).first()

def create_transcript(db: Session, meeting_id: int, content: str):
    transcript = Transcript(meeting_id=meeting_id, content=content)
    db.add(transcript)
    db.commit()
    db.refresh(transcript)
    return transcript

