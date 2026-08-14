from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


# 1. The Link Table
class TaskTag(SQLModel, table=True):
    task_id: int | None = Field(default=None, foreign_key="task.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)


# 2. The Tag Model
class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    tasks: list["Task"] = Relationship(back_populates="tags", link_model=TaskTag)
