from fastapi import Depends, FastAPI, HTTPException

from database import SessionLocal, engine
from models import Base
from repositories import SQLTaskRepository, TaskRepository
from schemas import TaskCreate, TaskUpdate

Base.metadata.create_all(bind=engine)


app = FastAPI()


async def get_db():
    db = SessionLocal()
    try:
        yield SQLTaskRepository(db)
    finally:
        db.close()


@app.get("/todo/api/v1.0/tasks")
async def get_tasks(db: TaskRepository = Depends(get_db)):
    return {"tasks": db.list()}


@app.get("/todo/api/v1.0/tasks/{task_id}")
async def get_task(task_id: int, db: TaskRepository = Depends(get_db)):
    task = db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {"task": task}


@app.post("/todo/api/v1.0/tasks", status_code=201)
async def create_task(t: TaskCreate, db: TaskRepository = Depends(get_db)):
    task = db.add(t)

    return {"task": task}


@app.put("/todo/api/v1.0/tasks/{task_id}")
def update_task(
    task_id: int, t: TaskUpdate, db: TaskRepository = Depends(get_db)
):
    task = db.update(task_id, t)

    if task is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {"task": task}


@app.delete("/todo/api/v1.0/tasks/{task_id}")
async def delete_task(task_id: int, db: TaskRepository = Depends(get_db)):
    if not db.delete(task_id):
        raise HTTPException(status_code=404, detail="Not found")

    return {"result": True}
