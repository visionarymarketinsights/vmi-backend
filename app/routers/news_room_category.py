from typing import List
from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.models import NewsRoomCategory
from app.database import get_db
from pydantic import BaseModel
import os

router = APIRouter()

@router.get("/")
async def get_category(db: Session = Depends(get_db)):
    news_room_category_list = db.query(NewsRoomCategory).order_by(NewsRoomCategory.name.asc()).all()
    return {"data": news_room_category_list}

@router.get("/{category_id}")
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    news_room_category_data = db.query(NewsRoomCategory).filter(NewsRoomCategory.id == category_id).first()
    return {"data": news_room_category_data}

@router.get("/url/{category_url}")
async def get_category_by_url(category_url: str, db: Session = Depends(get_db)):
    news_room_category_data = db.query(NewsRoomCategory).filter(NewsRoomCategory.url == category_url).first()
    return {"data": news_room_category_data}

