from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.schemas.user import UserRead, UserCreate
from app.security import hash_password  # ← NEW: import our hashing function

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # Hash the password before storing it
    hashed_password = hash_password(user.password)  # ← NEW

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,  # ← Store the hash, not the password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/", response_model=list[UserRead])
def get_users(session: Session = Depends(get_session)):
    statement = select(User)
    results = session.exec(statement)
    return results.all()


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
