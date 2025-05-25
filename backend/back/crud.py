from sqlalchemy.orm import Session
from uuid import uuid4
from back import models, schemas


# --- Users ---




# --- Meetings ---

def create_meeting(db: Session, meeting: schemas.MeetingCreate):
    db_meeting = models.Meeting(**meeting.model_dump(include={"id", "title", "duration", "start_time"}))
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def get_meetings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meeting).offset(skip).limit(limit).all()


# --- Transcripts ---

def create_transcript(db: Session, transcript: schemas.TranscriptCreate):
    db_transcript = models.Transcript( **transcript.model_dump())
    db.add(db_transcript)
    db.commit()
    db.refresh(db_transcript)
    return db_transcript

def get_transcripts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transcript).offset(skip).limit(limit).all()


# --- Summaries ---

def create_summary(db: Session, summary: schemas.SummaryCreate):
    db_summary = models.Summary(**summary.model_dump())
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary

def get_summaries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Summary).offset(skip).limit(limit).all()


# --- Participants ---

def create_participant(db: Session, participant: schemas.ParticipantCreate):
    db_participant = models.Participant(id=uuid4(), **participant.model_dump())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_participants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Participant).offset(skip).limit(limit).all()


# --- Tasks ---

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(id=uuid4(), **task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

