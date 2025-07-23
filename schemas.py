from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class TaskOut(BaseModel):
    id: str
    title: str
    status: str
    created_at: datetime
    priority: int

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    status: Literal["pending", "in_progress", "done"]
