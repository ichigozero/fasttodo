import pytest

from app.repositories.inmem import InMemoryTaskRepository
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task import TaskService


@pytest.fixture
def task_svc(default_tasks: list[Task]) -> TaskService:
    t = InMemoryTaskRepository(default_tasks)
    return TaskService(t)


def test_add_task(task_svc: TaskService):
    got = task_svc.create(
        TaskCreate(
            title="Learn FastAPI", description="FastAPI is easy to learn"
        )
    )
    want = Task(
        id=3,
        title="Learn FastAPI",
        description="FastAPI is easy to learn",
        is_done=False,
    )

    assert got == want


def test_get_tasks(task_svc: TaskService, default_tasks: list[Task]):
    got = task_svc.list()
    want = default_tasks

    assert got == want


def test_get_task(task_svc: TaskService, default_tasks: list[Task]):
    got = task_svc.get(task_id=1)
    want = default_tasks[0]

    assert got == want


def test_get_missing_task(task_svc: TaskService):
    got = task_svc.get(task_id=3)
    want = None

    assert got == want


def test_update_task(task_svc: TaskService):
    got = task_svc.update(
        task_id=1,
        task=TaskUpdate(
            title="Updated title",
            description="Updated description",
            is_done=True,
        ),
    )
    want = Task(
        id=1,
        title="Updated title",
        description="Updated description",
        is_done=True,
    )

    assert got == want


def test_update_missing_task(task_svc: TaskService):
    got = task_svc.update(
        task_id=3,
        task=TaskUpdate(
            title="Updated title",
            description="Updated description",
            is_done=True,
        ),
    )
    want = None

    assert got == want


def test_delete_task(task_svc: TaskService):
    got = task_svc.delete(task_id=1)
    want = True

    assert got == want


def test_delete_missing_task(task_svc: TaskService):
    got = task_svc.delete(task_id=3)
    want = False

    assert got == want
