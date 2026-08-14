from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.task import Task


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    tasks: list["Task"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all,delete-orphan"}
    )
