from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# --- Users ---

class UserBase(BaseModel):
    title: Optional[str]
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True


# --- Meetings ---

class MeetingBase(BaseModel):
    title: Optional[str]
    duration: Optional[float]
    start_time: Optional[datetime]
    user_id: UUID

class MeetingCreate(MeetingBase):
    pass

class Meeting(MeetingBase):
    id: UUID

    class Config:
        orm_mode = True


# --- Transcripts ---

class TranscriptBase(BaseModel):
    filename: str
    content: Optional[str]
    meeting_id: UUID

class TranscriptCreate(TranscriptBase):
    pass

class Transcript(TranscriptBase):
    id: UUID

    class Config:
        orm_mode = True


# --- Summaries ---

class SummaryBase(BaseModel):
    content: Optional[str]
    meeting_id: UUID

class SummaryCreate(SummaryBase):
    pass

class Summary(SummaryBase):
    id: UUID

    class Config:
        orm_mode = True


# --- Participants ---

class ParticipantBase(BaseModel):
    meeting_id: UUID
    user_id: Optional[UUID]
    email: Optional[EmailStr]

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: UUID

    class Config:
        orm_mode = True


# --- Tasks ---

class TaskBase(BaseModel):
    description: str
    status: Optional[str] = "todo"  # todo or done
    participant_id: Optional[UUID]
    meeting_id: UUID

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: UUID

    class Config:
        orm_mode = True

