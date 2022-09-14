from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm import Session

from schemas import Task, TaskCreate, TaskUpdate
from models import Task as TaskModel


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: TaskCreate) -> Task:
        raise NotImplementedError

    @abstractmethod
    def get(self, task_id: int) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def update(
        self, task_id: int, task: TaskUpdate
    ) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        raise NotImplementedError


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add(self, t: TaskCreate) -> Task:
        try:
            id = self.tasks[-1].id + 1
        except IndexError:
            id = 1

        task = Task(
            id=id, title=t.title, description=t.description, is_done=False
        )
        self.tasks.append(task)

        return task

    def get(self, task_id: int) -> Task | None:
        task = [task for task in self.tasks if task.id == task_id]
        if len(task) == 0:
            return None

        return task[0]

    def list(self) -> List[Task]:
        return self.tasks

    def update(
        self, task_id: int, t: TaskUpdate
    ) -> Task | None:
        task = [task for task in self.tasks if task.id == task_id]
        if len(task) == 0:
            return None

        task[0].title = t.title
        task[0].description = t.description
        task[0].is_done = t.is_done

        return task[0]

    def delete(self, task_id: int) -> bool:
        task = [task for task in self.tasks if task.id == task_id]
        if len(task) == 0:
            return False

        self.tasks.remove(task[0])

        return True


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
        return (
            self.db.query(TaskModel)
            .filter(TaskModel.id == task_id)
            .first()
        )

    def list(self) -> List[Task]:
        return self.db.query(TaskModel).all()

    def update(
        self, task_id: int, task: TaskUpdate
    ) -> Task | None:
        t = (
            self.db.query(TaskModel)
            .filter(TaskModel.id == task_id)
            .first()
        )
        if t is None:
            return None

        t.title = task.title
        t.description = task.description
        t.is_done = task.is_done

        self.db.commit()

        return t

    def delete(self, task_id: int) -> bool:
        rows = (
            self.db.query(TaskModel)
            .filter(TaskModel.id == task_id)
            .delete()
        )

        return rows > 0
