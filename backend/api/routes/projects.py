"""
Project CRUD API routes
"""
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings
from database.models import Base, NovelProject

router = APIRouter(prefix="/projects", tags=["projects"])

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = "draft"


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


def project_to_dict(p: NovelProject) -> dict:
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "genre": p.genre,
        "status": p.status,
        "content": p.content,
        "word_count": p.word_count,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
        "user_id": p.user_id,
    }


@router.post("", status_code=201)
def create_project(body: ProjectCreate, db: Session = Depends(get_db)):
    project = NovelProject(
        id=str(uuid.uuid4()),
        title=body.title,
        description=body.description,
        genre=body.genre,
        content=body.content,
        status=body.status or "draft",
        word_count=len(body.content.split()) if body.content else 0,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project_to_dict(project)


@router.get("")
def list_projects(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(NovelProject)
    if status:
        query = query.filter(NovelProject.status == status)
    return [project_to_dict(p) for p in query.all()]


@router.get("/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(NovelProject).filter(NovelProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_to_dict(project)


@router.put("/{project_id}")
def update_project(project_id: str, body: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(NovelProject).filter(NovelProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    if body.content is not None:
        project.word_count = len(body.content.split())
    db.commit()
    db.refresh(project)
    return project_to_dict(project)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(NovelProject).filter(NovelProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
