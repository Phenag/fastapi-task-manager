from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Tag
from app.schemas.tag import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagRead, status_code=201)
def create_tag(tag_data: TagCreate, session: Session = Depends(get_session)):
    # Check if tag already exists (since name is unique)
    existing_tag = session.exec(select(Tag).where(Tag.name == tag_data.name)).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")

    new_tag = Tag(name=tag_data.name)
    session.add(new_tag)
    session.commit()
    session.refresh(new_tag)
    return new_tag


@router.get("/", response_model=list[TagRead])
def get_tags(session: Session = Depends(get_session)):
    tags = session.exec(select(Tag)).all()
    return tags
