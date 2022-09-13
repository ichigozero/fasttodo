from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
        "done": False,
    },
    {
        "id": 2,
        "title": "Learn Python",
        "description": "Need to find a good Python tutorial on the web",
        "done": False,
    },
]


@app.get("/todo/api/v1.0/tasks")
async def get_tasks():
    return {"tasks": tasks}


@app.get("/todo/api/v1.0/tasks/{task_id}")
async def get_task(task_id: int):
    task = [task for task in tasks if task["id"] == task_id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Not found")

    return {"task": task[0]}


class NewTask(BaseModel):
    title: str
    description: str = ""


@app.post("/todo/api/v1.0/tasks", status_code=201)
async def create_task(task: NewTask):
    t = {
        "id": tasks[-1]["id"] + 1,
        "title": task.title,
        "description": task.description,
        "done": False,
    }
    tasks.append(t)

    return {"task": t}


class UpdatedTask(BaseModel):
    title: str
    description: str
    done: bool


@app.put("/todo/api/v1.0/tasks/{task_id}")
def update_task(task_id: int, task: UpdatedTask):
    t = [task for task in tasks if task["id"] == task_id]
    if len(t) == 0:
        raise HTTPException(status_code=404, detail="Not found")

    t[0]["title"] = task.title
    t[0]["description"] = task.description
    t[0]["done"] = task.done

    return {"task": t}


@app.delete("/todo/api/v1.0/tasks/{task_id}")
async def delete_task(task_id: int):
    task = [task for task in tasks if task["id"] == task_id]
    if len(task) == 0:
        raise HTTPException(status_code=404, detail="Not found")
    tasks.remove(task[0])

    return {"result": True}
