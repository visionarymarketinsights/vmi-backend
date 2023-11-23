from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Category, PressRelease
from app.database import get_db
from sqlalchemy import DateTime, func

router = APIRouter()


class CreatePressReleaseRequest(BaseModel):
    category_id: int
    description: str
    summary: str
    title: str
    meta_title: str
    meta_desc: str
    meta_keyword: str
    report_id: int
    url: str
    cover_img: str
    created_date: str


class UpdatePressReleaseRequest(BaseModel):
    id: int
    category_int: int
    description: str
    summary: str
    title: str
    meta_title: str
    meta_desc: str
    meta_keyword: str
    report_id: int
    url: str
    cover_img: str
    created_date: str


class GetPressRelease(BaseModel):
    id: int
    title: str
    category_id: int
    category_url: str
    category_name: str
    category_abr: str
    summary: str
    created_date: str
    url: str
    cover_img: str


@router.get("/")
async def get_press_releases(db: Session = Depends(get_db)):
    press_releases = (
        db.query(PressRelease)
        .join(Category, PressRelease.category_id == Category.id)
        .with_entities(
            PressRelease.id,
            PressRelease.category_id,
            Category.url.label("category_url"),
            Category.abr.label("category_abr"),
            Category.name.label("category_name"),
            PressRelease.summary,
            PressRelease.title,
            PressRelease.created_date,
            PressRelease.url,
            PressRelease.cover_img,
        )
        .all()
    )
    press_release_list = [
        GetPressRelease(
            id=press_release.id,
            title=press_release.title,
            category_id=press_release.category_id,
            category_name=press_release.category_name,
            category_url=press_release.category_url,
            category_abr=press_release.category_abr,
            summary=press_release.summary,
            created_date=press_release.created_date,
            url=press_release.url,
            cover_img=press_release.cover_img,
        )
        for press_release in press_releases
    ]
    return {"data": press_release_list}


@router.get("/category/category_count")
async def get_press_release_category_count(db: Session = Depends(get_db)):
    query = (
        db.query(
            Category.id.label("category_id"),
            Category.url.label("category_url"),
            Category.abr.label("category_abr"),
            Category.name.label("category_name"),
            Category.back_cover.label("category_back_cover"),
            Category.icon.label("category_icon"),
            func.count(PressRelease.category_id).label("count"),
        )
        .join(Category, PressRelease.category_id == Category.id)
        .group_by(Category.id)
        .all()
    )
    result = [
        {
            "category_id": category_id,
            "category_url": category_url,
            "category_abr": category_abr,
            "category_name": category_name,
            "category_back_cover": category_back_cover,
            "category_icon": category_icon,
            "count": count,
        }
        for category_id, category_url, category_abr, category_name, category_back_cover, category_icon, count in query
    ]
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
        .join(Category, PressRelease.category_id == Category.id)
        .with_entities(
            PressRelease.id,
            PressRelease.category_id,
            Category.url.label("category_url"),
            Category.name.label("category_name"),
            Category.abr.label("category_abr"),
            PressRelease.summary,
            PressRelease.title,
            PressRelease.created_date,
            PressRelease.url,
            PressRelease.cover_img,
        )
        .order_by(func.cast(PressRelease.created_date, DateTime).desc())
        .offset(offset)
        .limit(per_page)
        .all()
    )

    press_release_list = [
        GetPressRelease(
            id=press_release.id,
            category_id=press_release.category_id,
            category_url=press_release.category_url,
            category_name=press_release.category_name,
            category_abr=press_release.category_abr,
            summary=press_release.summary,
            title=press_release.title,
            created_date=press_release.created_date,
            url=press_release.url,
            cover_img=press_release.cover_img,
        )
        for press_release in press_releases
    ]

    return {"data": press_release_list}


@router.get("/category/{category_url}")
async def get_press_release_by_category_url(
    category_url: str,
    page: int,
    per_page: int,
    db: Session = Depends(get_db),
):
    offset = (page - 1) * per_page

    press_releases = (
        # db.query(Report)
        db.query(PressRelease)
        .join(Category, PressRelease.category_id == Category.id)
        .with_entities(
            PressRelease.id,
            PressRelease.category_id,
            Category.abr.label("category_abr"),
            Category.url.label("category_url"),
            Category.name.label("category_name"),
            PressRelease.summary,
            PressRelease.title,
            PressRelease.created_date,
            PressRelease.url,
            PressRelease.cover_img,
        )
        .filter(Category.url == category_url)
        .offset(offset)
        .limit(per_page)
        .all()
    )

    press_release_list = [
        GetPressRelease(
            id=press_release.id,
            title=press_release.title,
            category_id=press_release.category_id,
            category_name=press_release.category_name,
            category_url=press_release.category_url,
            category_abr=press_release.category_abr,
            summary=press_release.summary,
            created_date=press_release.created_date,
            url=press_release.url,
            cover_img=press_release.cover_img,
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


# @router.get("/url/{press_release_url}")
# async def get_press_release_by_url(
#     press_release_url: int, db: Session = Depends(get_db)
# ):
#     press_release = (
#         db.query(PressRelease, Category.name)
#         .join(Category, PressRelease.category_id == Category.id)
#         .filter(PressRelease.url == press_release_url)
#         .first()
#     )
#     if press_release:
#         press_release_data, category_name = press_release
#         press_release_data_dict = dict(press_release_data.__dict__)
#         press_release_data_dict["category_name"] = category_name
#         return {"data": press_release_data_dict}
#     else:
#         return {"data": None}


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
