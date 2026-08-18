from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.task import Task


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(index=True, unique=True)

    email: str = Field(index=True, unique=True)

    password_hash: str = Field(nullable=False)

    tasks: List["Task"] = Relationship(back_populates="user")
