from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str = ""


class Task(TaskBase):
    id: int
    is_done: bool


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    is_done: bool
