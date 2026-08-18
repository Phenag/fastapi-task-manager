from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select
from app.database import get_session
from app.dependencies import get_current_user
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])


## Returning 403 says "this exists but you can't access it" — which leaks information. Returning 404 says "this doesn't exist for you"
@router.get("/", response_model=list[TaskRead])
def get_tasks(
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),  # ← Protected!
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    """Get all tasks (requires authentication)."""
    results = session.exec(
        select(Task)
        .where(Task.user_idid == current_user.id)
        .limit(limit)
        .offset(offset)
    ).all()
    return results


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),  # ← Protected!
):
    """Get a specific task by ID (requires authentication)."""
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskRead, status_code=201)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),  # ← Protected!
):
    """Create a new task (requires authentication)."""
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id,  # ← Automatically assign to current user!
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),  # ← Protected!
):
    """Update a task (requires authentication)."""
    db_task = session.get(Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),  # ← Protected!
):
    """Delete a task (requires authentication)."""
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
