import pytest

from app.schemas.task import Task


@pytest.fixture
def default_tasks() -> list[Task]:
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
