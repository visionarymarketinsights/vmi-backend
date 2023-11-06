from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.models import Report, ReportImage  # Import the ReportImage model
from app.database import get_db
from pydantic import BaseModel
import os

router = APIRouter()


class CreateReportImageRequest(BaseModel):
    report_id: int
    img_name: str
    img_file: str

@router.post("/")
async def create_report_image(image: CreateReportImageRequest, db: Session = Depends(get_db)):
    # Check if the associated report exists
    report = db.query(Report).filter(Report.id == image.report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    db_image = ReportImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return {"data": db_image}

@router.put("/{image_id}")
async def update_report_image(image_id: int, image: CreateReportImageRequest, db: Session = Depends(get_db)):
    existing_image = db.query(ReportImage).filter(ReportImage.id == image_id).first()
    if existing_image is None:
        raise HTTPException(status_code=404, detail="Report Image not found")

    # Update image attributes
    existing_image.report_id = image.report_id
    existing_image.img_name = image.img_name
    existing_image.img_file = image.img_file

    db.commit()
    db.refresh(existing_image)
    return {"data": existing_image}

@router.delete("/{image_id}")
async def delete_report_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ReportImage).filter(ReportImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Report Image not found")

    db.delete(image)
    db.commit()
    return {"message": "Report Image deleted"}


