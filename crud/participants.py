from sqlalchemy.orm import Session
from back.models import Participant

def get_participant(db: Session, participant_id: int):
    return db.query(Participant).filter(Participant.id == participant_id).first()

def create_participant(db: Session, name: str, meeting_id: int):
    participant = Participant(name=name, meeting_id=meeting_id)
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant

