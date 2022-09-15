from typing import List

import pytest

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.repositories.inmem import InMemoryTaskRepository
from app.routers import task
from app.schemas.task import Task
from app.services.task import TaskService

app = FastAPI()
app.include_router(task.router)

client = TestClient(app)


def default_tasks() -> List[Task]:
    return [
        Task(
            id=1,
            title="Buy groceries",
            description="Milk, Cheese, Pizza, Fruit, Tylenol",
            is_done=False,
        ),
        Task(
            id=2,
            title="Learn Python",
            description="Need to find a good Python tutorial on the web",
            is_done=False,
        ),
    ]


@pytest.fixture
def task_svc():
    def mock_svc() -> TaskService:
        t = InMemoryTaskRepository(default_tasks())
        return TaskService(t)

    app.dependency_overrides[task.task_svc] = mock_svc
    yield
    app.dependency_overrides = {}


def test_add_task(task_svc):
    res = client.post(
        "/api/v1.0/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "FastAPI is easy to learn",
        },
    )

    assert res.status_code == 201
    assert res.json() == {
        "task": {
            "id": 3,
            "title": "Learn FastAPI",
            "description": "FastAPI is easy to learn",
            "is_done": False,
        },
    }


def test_get_tasks(task_svc):
    res = client.get("/api/v1.0/tasks")

    assert res.status_code == 200
    assert res.json() == {"tasks": jsonable_encoder(default_tasks())}


def test_get_task(task_svc):
    res = client.get("/api/v1.0/tasks/1")

    assert res.status_code == 200
    assert res.json() == {"task": jsonable_encoder(default_tasks()[0])}


def test_get_missing_task(task_svc):
    res = client.get("/api/v1.0/tasks/3")

    assert res.status_code == 404


def test_update_task(task_svc):
    res = client.put(
        "/api/v1.0/tasks/1",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "is_done": True,
        },
    )

    assert res.status_code == 200
    assert res.json() == {
        "task": {
            "id": 1,
            "title": "Updated title",
            "description": "Updated description",
            "is_done": True,
        }
    }


def test_update_missing_task(task_svc):
    res = client.put(
        "/api/v1.0/tasks/3",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "is_done": True,
        },
    )

    assert res.status_code == 404


def test_delete_task(task_svc):
    res = client.delete("/api/v1.0/tasks/1")

    assert res.status_code == 200
    assert res.json() == {"result": True}


def test_delete_missing_task(task_svc):
    res = client.delete("/api/v1.0/tasks/3")

    assert res.status_code == 404
