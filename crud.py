from sqlalchemy.orm import Session
from uuid import uuid4
from back import models, schemas


# --- Users ---

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(id=uuid4(), **user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# --- Meetings ---

def create_meeting(db: Session, meeting: schemas.MeetingCreate):
    db_meeting = models.Meeting(id=uuid4(), **meeting.dict())
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def get_meetings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meeting).offset(skip).limit(limit).all()


# --- Transcripts ---

def create_transcript(db: Session, transcript: schemas.TranscriptCreate):
    db_transcript = models.Transcript(id=uuid4(), **transcript.dict())
    db.add(db_transcript)
    db.commit()
    db.refresh(db_transcript)
    return db_transcript

def get_transcripts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transcript).offset(skip).limit(limit).all()


# --- Summaries ---

def create_summary(db: Session, summary: schemas.SummaryCreate):
    db_summary = models.Summary(id=uuid4(), **summary.dict())
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary

def get_summaries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Summary).offset(skip).limit(limit).all()


# --- Participants ---

def create_participant(db: Session, participant: schemas.ParticipantCreate):
    db_participant = models.Participant(id=uuid4(), **participant.dict())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_participants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Participant).offset(skip).limit(limit).all()


# --- Tasks ---

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(id=uuid4(), **task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

