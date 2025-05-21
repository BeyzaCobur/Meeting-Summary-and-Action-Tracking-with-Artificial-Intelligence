import uuid
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base  # Base, SQLAlchemy declarative base'in

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    email = Column(String, unique=True)

    meetings = relationship("Meeting", back_populates="user")
    participants = relationship("Participant", back_populates="user")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    duration = Column(Float)
    start_time = Column(DateTime)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="meetings")

    transcripts = relationship("Transcript", back_populates="meeting", cascade="all, delete")
    summaries = relationship("Summary", back_populates="meeting", cascade="all, delete")
    participants = relationship("Participant", back_populates="meeting", cascade="all, delete")
    tasks = relationship("Task", back_populates="meeting", cascade="all, delete")


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String)
    content = Column(Text)

    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"))
    meeting = relationship("Meeting", back_populates="transcripts")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text)

    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"))
    meeting = relationship("Meeting", back_populates="summaries")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    email = Column(String)

    meeting = relationship("Meeting", back_populates="participants")
    user = relationship("User", back_populates="participants")
    tasks = relationship("Task", back_populates="participant", cascade="all, delete")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text)
    status = Column(String, nullable=False)
    __table_args__ = (
        CheckConstraint("status IN ('todo', 'done')", name="check_task_status"),
    )

    participant_id = Column(UUID(as_uuid=True), ForeignKey("participants.id", ondelete="SET NULL"), nullable=True)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="CASCADE"))

    participant = relationship("Participant", back_populates="tasks")
    meeting = relationship("Meeting", back_populates="tasks")

