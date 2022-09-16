from sqlalchemy.orm import Session

from models.task import Task as TaskModel
from schemas.task import Task, TaskCreate, TaskUpdate

from .base import TaskRepository


class SQLTaskRepository(TaskRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, t: TaskCreate) -> Task:
        task = TaskModel(title=t.title, description=t.description)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def get(self, task_id: int) -> Task | None:
        return self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

    def list(self) -> list[Task]:
        return self.db.query(TaskModel).all()

    def update(self, task_id: int, task: TaskUpdate) -> Task | None:
        t = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if t is None:
            return None

        t.title = task.title
        t.description = task.description
        t.is_done = task.is_done

        self.db.commit()

        return t

    def delete(self, task_id: int) -> bool:
        rows = (
            self.db.query(TaskModel).filter(TaskModel.id == task_id).delete()
        )

        return rows > 0
