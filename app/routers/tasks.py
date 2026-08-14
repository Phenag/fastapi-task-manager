from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.database import get_session
from app.models import Tag, Task
from app.schemas import TaskUpdate, TaskRead, TaskCreate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskRead])
def get_tasks(
    session: Session = Depends(get_session),
    completed: bool | None = None,
    limit: int = Query(default=10, gt=0, le=100),
    offset: int = Query(default=0, ge=0),
    sort: str = Query(default="newest", pattern="^(newest|oldest)$"),
):
    statement = select(Task)
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    if sort == "newest":
        statement = statement.order_by(Task.id.desc())
    else:
        statement = statement.order_by(Task.id)
    statement = statement.offset(offset).limit(limit)
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
        user_id=task.user_id,
    )
    # Fetch and attach tags if tag_ids were provided in the request
    if task.tag_ids:
        tags = session.exec(select(Tag).where(Tag.id.in_(task.tag_ids))).all()
        new_task.tags = tags
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

    # 1. Exclude tag_ids so sqlmodel_update doesn't break on a non-column field
    task_data = task.model_dump(exclude_unset=True, exclude={"tag_ids"})
    db_task.sqlmodel_update(task_data)

    # 2. If tag_ids was sent in the request, update the tags relationship
    if task.tag_ids is not None:
        tags = session.exec(select(Tag).where(Tag.id.in_(task.tag_ids))).all()
        db_task.tags = tags

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
