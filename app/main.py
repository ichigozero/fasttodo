from fastapi import FastAPI

from app.config.database import create_tables
from app.routers import task

create_tables()

app = FastAPI()
app.include_router(task.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
