from pydantic import BaseModel


class TaskPublic(BaseModel):
    id: int
    title: str
    completed: bool


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    tasks: list[TaskPublic]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # ← NEW: accept password when creating user