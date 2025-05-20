from sqlalchemy.orm import Session
from back.models import Task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, meeting_id: int, content: str):
    task = Task(meeting_id=meeting_id, content=content)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

