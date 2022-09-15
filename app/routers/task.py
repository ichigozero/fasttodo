from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from repositories.sql import SQLTaskRepository
from schemas.task import TaskCreate, TaskUpdate
from services.task import TaskService

router = APIRouter(prefix="/api/v1.0", tags=["tasks"])


def task_svc(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(SQLTaskRepository(db))


@router.get("/tasks")
async def get_tasks(svc: TaskService = Depends(task_svc)):
    return {"tasks": svc.list()}


@router.get("/tasks/{task_id}")
async def get_task(task_id: int, svc: TaskService = Depends(task_svc)):
    task = svc.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {"task": task}


@router.post("/tasks", status_code=201)
async def create(t: TaskCreate, svc: TaskService = Depends(task_svc)):
    task = svc.create(t)
    return {"task": task}


@router.put("/tasks/{task_id}")
async def update(
    task_id: int, t: TaskUpdate, svc: TaskService = Depends(task_svc)
):
    task = svc.update(task_id, t)
    if task is None:
        raise HTTPException(status_code=404, detail="Not found")

    return {"task": task}


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, svc: TaskService = Depends(task_svc)):
    if not svc.delete(task_id):
        raise HTTPException(status_code=404, detail="Not found")

    return {"result": True}
