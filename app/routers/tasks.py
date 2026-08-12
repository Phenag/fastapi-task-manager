from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.task import Task, TaskCreate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)




tasks = []
next_id = 1


@router.post("/", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    global next_id

    new_task = Task(
        id=next_id,
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    tasks.append(new_task)
    next_id += 1

    return new_task


@router.get("/", response_model=list[Task])
def get_tasks():
    return tasks


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int):

    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    updated_task: TaskCreate
):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            new_task = Task(
                id=task_id,
                title=updated_task.title,
                description=updated_task.description,
                completed=updated_task.completed
            )

            tasks[index] = new_task

            return new_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@router.delete("/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted",
                "task": deleted_task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )