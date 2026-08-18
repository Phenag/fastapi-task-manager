from pydantic import BaseModel
from typing import Optional, List


## what the client will send
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    tag_ids: List[int] = []
    # DO NOT include user_id here - it's auto-assigned from token


## what the client will send to update
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    tag_ids: Optional[List[int]] = None
    # DO NOT include user_id here either


## nested user info shown inside a task
class UserPublic(BaseModel):
    id: int
    username: str
    email: str


## what the client will read
class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: int  # This is fine for reading
    user: UserPublic
    tag_ids: List[int] = []

    class Config:
        from_attributes = True
