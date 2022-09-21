from abc import ABC, abstractmethod

from app.schemas.task import Task, TaskCreate, TaskUpdate


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: TaskCreate) -> Task:
        raise NotImplementedError

    @abstractmethod
    def get(self, task_id: int) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def update(self, task_id: int, task: TaskUpdate) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        raise NotImplementedError
