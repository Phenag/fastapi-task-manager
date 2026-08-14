from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

# 1. Import TaskTag at RUNTIME because link_model needs the actual class
from app.models.tag import TaskTag

# 2. Keep User and Tag inside TYPE_CHECKING to prevent circular imports
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.tag import Tag


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="tasks")
    # Add this line for the Tag relationship:
    tags: list["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
