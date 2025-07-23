from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import List, Optional
from database import get_db, engine
from models import Base, Task
from schemas import TaskOut, TaskUpdate

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Task API Running"}

# GET /tasks/next
@app.get("/tasks/next", response_model=Optional[TaskOut])
def get_next_task(db: Session = Depends(get_db)):
    task = db.query(Task)\
             .filter(Task.status == "pending")\
             .order_by(asc(Task.priority), asc(Task.created_at))\
             .first()
    return task

# PUT /tasks/{task_id}/status
@app.put("/tasks/{task_id}/status", response_model=TaskOut)
def update_task_status(task_id: str, update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    status_flow = {"pending": 1, "in_progress": 2, "done": 3}
    current = status_flow.get(task.status, 0)
    new = status_flow.get(update.status, 0)

    if new < current:
        raise HTTPException(status_code=400, detail="Status regression not allowed")

    task.status = update.status
    db.commit()
    db.refresh(task)
    return task

# GET /tasks/pending
@app.get("/tasks/pending", response_model=List[TaskOut])
def get_pending_tasks(
    sort_by: Optional[str] = Query("created_at"),
    sort_order: Optional[str] = Query("asc"),
    limit: Optional[int] = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    if not hasattr(Task, sort_by):
        raise HTTPException(status_code=400, detail="Invalid sort field")

    column = getattr(Task, sort_by)
    sort_column = desc(column) if sort_order == "desc" else asc(column)

    tasks = db.query(Task)\
              .filter(Task.status == "pending")\
              .order_by(sort_column)\
              .limit(limit)\
              .all()
    return tasks
