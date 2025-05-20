from sqlalchemy.orm import Session
from back.models import Summary

def get_summary(db: Session, summary_id: int):
    return db.query(Summary).filter(Summary.id == summary_id).first()

def create_summary(db: Session, meeting_id: int, content: str):
    summary = Summary(meeting_id=meeting_id, content=content)
    db.add(summary)
    db.commit()
    db.refresh(summary)
    return summary

