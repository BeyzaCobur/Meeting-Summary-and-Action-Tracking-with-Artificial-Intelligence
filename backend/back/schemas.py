from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# --- Users ---



# --- Meetings ---

class MeetingBase(BaseModel):
    title: Optional[str]
    duration: Optional[float]
    start_time: Optional[datetime]
    summaries: Optional[List[dict]] = None 
    tasks: Optional[List[dict]]
    

class MeetingCreate(MeetingBase):
    id: UUID
    
    
class Meeting(MeetingBase):
    id: UUID

    class Config:
        orm_mode = True


# --- Transcripts ---

class TranscriptBase(BaseModel):
    id: Optional[UUID] = None
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

