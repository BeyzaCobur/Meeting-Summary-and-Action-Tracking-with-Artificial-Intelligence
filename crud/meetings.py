from sqlalchemy.orm import Session
from back.models import Meeting

def get_meeting(db: Session, meeting_id: int):
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()

def create_meeting(db: Session, title: str):
    meeting = Meeting(title=title)
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting

