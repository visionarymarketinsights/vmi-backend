from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import PressRelease
from app.database import get_db
from sqlalchemy import DateTime, func

router = APIRouter()


class CreatePressReleaseRequest(BaseModel):
    category: str
    description: str
    summary: str
    title: str
    meta_title: str
    meta_desc: str
    meta_keyword: str
    created_date: str


class UpdatePressReleaseRequest(BaseModel):
    id: int
    category: str
    description: str
    summary: str
    title: str
    meta_title: str
    meta_desc: str
    meta_keyword: str
    created_date: str


class PressReleaseListSchema(BaseModel):
    id: int
    title: str
    category: str
    summary: str
    created_date: str


@router.get("/")
async def get_press_releases(db: Session = Depends(get_db)):
    press_releases = (
        db.query(PressRelease)
        .with_entities(
            PressRelease.id,
            PressRelease.category,
            PressRelease.summary,
            PressRelease.title,
        )
        .all()
    )
    press_release_list = [
        PressReleaseListSchema(
            id=press_release.id,
            title=press_release.title,
            category=press_release.category,
            summary=press_release.summary,
            created_date=press_release.created_date,
        )
        for press_release in press_releases
    ]
    return {"data": press_release_list}


@router.get("/category/category_count")
async def get_press_release_category_count(db: Session = Depends(get_db)):
    query = (
        db.query(PressRelease.category, func.count(PressRelease.category))
        .group_by(PressRelease.category)
        .all()
    )
    result = [{"category": category, "count": count} for category, count in query]
    return {"data": result}


@router.get("/latest")
async def get_latest_reports(
    page: int,
    per_page: int,
    db: Session = Depends(get_db),
):
    offset = (page - 1) * per_page

    press_releases = (
        db.query(PressRelease)
        .with_entities(
            PressRelease.id,
            PressRelease.category,
            PressRelease.summary,
            PressRelease.title,
            PressRelease.created_date,
        )
        .order_by(func.cast(PressRelease.created_date, DateTime).desc())
        .offset(offset)
        .limit(per_page)
        .all()
    )

    press_release_list = [
        PressReleaseListSchema(
            id=press_release.id,
            title=press_release.title,
            category=press_release.category,
            summary=press_release.summary,
            created_date=press_release.created_date,
        )
        for press_release in press_releases
    ]

    return {"data": press_release_list}


@router.get("/category/{category}")
async def get_press_release_by_category(
    category: str,
    page: int,
    per_page: int,
    db: Session = Depends(get_db),
):
    if category is None:
        offset = (page - 1) * per_page

        press_releases = (
            # db.query(Report)
            db.query(PressRelease)
            .with_entities(
                PressRelease.id,
                PressRelease.category,
                PressRelease.summary,
                PressRelease.title,
                PressRelease.created_date,
            )
            .offset(offset)
            .limit(per_page)
            .all()
        )
    else:
        # Calculate the offset to skip records based on the page and per_page values
        offset = (page - 1) * per_page

        press_releases = (
            # db.query(Report)
            db.query(PressRelease)
            .with_entities(
                PressRelease.id,
                PressRelease.category,
                PressRelease.summary,
                PressRelease.title,
                PressRelease.created_date,
            )
            .filter(PressRelease.category == category)
            .offset(offset)
            .limit(per_page)
            .all()
        )

    press_release_list = [
        PressReleaseListSchema(
            id=press_release.id,
            title=press_release.title,
            category=press_release.category,
            summary=press_release.summary,
            created_date=press_release.created_date,
        )
        for press_release in press_releases
    ]

    return {"data": press_release_list}


@router.get("/{press_release_id}")
async def get_press_release_by_id(press_release_id: int, db: Session = Depends(get_db)):
    press_release = (
        db.query(PressRelease).filter(PressRelease.id == press_release_id).first()
    )
    return {"data": press_release}


@router.post("/")
async def create_press_release(
    press_release: CreatePressReleaseRequest, db: Session = Depends(get_db)
):
    db_press_release = PressRelease(**press_release.dict())
    db.add(db_press_release)
    db.commit()
    db.refresh(db_press_release)
    return {"data": db_press_release}


@router.put("/{press_release_id}")
async def update_press_release(
    new_press_release: UpdatePressReleaseRequest, db: Session = Depends(get_db)
):
    existing_press_release = (
        db.query(PressRelease).filter(PressRelease.id == new_press_release.id).first()
    )
    if existing_press_release is None:
        raise HTTPException(status_code=404, detail="Press Release not found")

    for attr, value in new_press_release.dict().items():
        setattr(existing_press_release, attr, value)

    db.commit()
    db.refresh(existing_press_release)
    return {"data": existing_press_release}


@router.delete("/{press_release_id}")
async def delete_press_release(press_release_id: int, db: Session = Depends(get_db)):
    press_release = (
        db.query(PressRelease).filter(PressRelease.id == press_release_id).first()
    )
    if press_release is None:
        raise HTTPException(status_code=404, detail="Press Release not found")

    db.delete(press_release)
    db.commit()
    return {"message": "Press Release deleted"}
