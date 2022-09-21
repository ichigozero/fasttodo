from app.repositories.base import TaskRepository
from app.schemas.task import Task, TaskCreate, TaskUpdate


class InMemoryTaskRepository(TaskRepository):
    def __init__(self, tasks: list[Task] = []) -> None:
        self._tasks: list[Task] = tasks

    def add(self, t: TaskCreate) -> Task:
        try:
            id = self._tasks[-1].id + 1
        except IndexError:
            id = 1

        task = Task(
            id=id, title=t.title, description=t.description, is_done=False
        )
        self._tasks.append(task)

        return task

    def get(self, task_id: int) -> Task | None:
        task = [task for task in self._tasks if task.id == task_id]
        if len(task) == 0:
            return None

        return task[0]

    def list(self) -> list[Task]:
        return self._tasks

    def update(self, task_id: int, t: TaskUpdate) -> Task | None:
        task = [task for task in self._tasks if task.id == task_id]
        if len(task) == 0:
            return None

        task[0].title = t.title
        task[0].description = t.description
        task[0].is_done = t.is_done

        return task[0]

    def delete(self, task_id: int) -> bool:
        task = [task for task in self._tasks if task.id == task_id]
        if len(task) == 0:
            return False

        self._tasks.remove(task[0])

        return True
