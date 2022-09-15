from typing import List

from repositories.base import TaskRepository
from schemas.task import Task, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, t: TaskRepository):
        self.task = t

    def create(self, task: TaskCreate) -> Task:
        return self.task.add(task)

    def get(self, task_id: int) -> Task | None:
        return self.task.get(task_id)

    def list(self) -> List[Task]:
        return self.task.list()

    def update(self, task_id: int, task: TaskUpdate) -> Task | None:
        return self.task.update(task_id, task)

    def delete(self, task_id: int) -> bool:
        return self.task.delete(task_id)