from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from repositories.base import TaskRepository
from repositories.inmem import InMemoryTaskRepository
from schema import NewTask, TaskUpdate

app = FastAPI()
repository = InMemoryTaskRepository()


async def db() -> TaskRepository:
    return repository


@app.get("/todo/api/v1.0/tasks")
async def get_tasks(db: TaskRepository = Depends(db)):
    return {"tasks": db.list()}


@app.get("/todo/api/v1.0/tasks/{task_id}")
async def get_task(task_id: int, db: TaskRepository = Depends(db)):
    task = db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {"task": task}


@app.post("/todo/api/v1.0/tasks", status_code=201)
async def create_task(t: NewTask, db: TaskRepository = Depends(db)):
    task = db.add(t)

    return {"task": task}


@app.put("/todo/api/v1.0/tasks/{task_id}")
def update_task(task_id: int, t: TaskUpdate, db: TaskRepository = Depends(db)):
    task = db.update(task_id, t)

    if task is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {"task": task}


@app.delete("/todo/api/v1.0/tasks/{task_id}")
async def delete_task(task_id: int, db: TaskRepository = Depends(db)):
    if not db.delete(task_id):
        raise HTTPException(status_code=404, detail="Not found")

    return {"result": True}
