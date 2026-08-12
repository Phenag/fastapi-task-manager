from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskRead])
def get_tasks(session: Session = Depends(get_session)):
    statement = select(Task)
    results = session.exec(statement)

    return results.all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    statement = select(Task).where(Task.id == task_id)

    results = session.exec(statement)

    task = results.first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, task: TaskUpdate, session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)

    db_task.sqlmodel_update(task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    statement = select(Task).where(Task.id == task_id)

    results = session.exec(statement)

    task = results.first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}
