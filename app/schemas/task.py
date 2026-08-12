from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


## what the client will send
class TaskCreate(BaseModel):
    title: str| None=None
    description: str | None = None
    completed: bool = False


class Task(TaskCreate):
    id: int

## what the client will send to update
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool = False


## what the client will read
class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
