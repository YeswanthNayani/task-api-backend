from sqlalchemy import Column, String, DateTime, Enum, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
import uuid

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=1)
