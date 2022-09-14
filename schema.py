from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str = ""
    done: bool


class NewTask(BaseModel):
    title: str
    description: str = ""


class TaskUpdate(BaseModel):
    title: str
    description: str
    done: bool
