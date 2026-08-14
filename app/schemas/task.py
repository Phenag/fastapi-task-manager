from pydantic import BaseModel

## what the client will send
class TaskCreate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool = False
    user_id: int

## what the client will send to update
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool = False

## nested user info shown inside a task
class UserPublic(BaseModel):
    id: int
    username: str
    email: str

## what the client will read
class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    user_id: int
    user: UserPublic

    class Config:
        from_attributes = True