from fastapi import FastAPI

from app.database import create_db_and_tables
from app.models import Task, User
from app.routers import tasks, users

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(tasks.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to my Task Manager API"}


@app.get("/about")
def about():
    return {"project": "Task Manager", "version": "1.0"}
