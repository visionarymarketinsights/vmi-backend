from fastapi import Depends, APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Report
from app.database import get_db
from sqlalchemy import func
import os
import io
from datetime import datetime
from PIL import Image

router = APIRouter()


class CreateReportRequest(BaseModel):
    title: str
    url: str
    category: str
    description: str
    toc: str
    highlights: str
    methodology: str
    meta_title: str
    meta_desc: str
    meta_keyword: str
    pages: str
    created_date: str


class UpdateReportRequest(BaseModel):
    id: int
    title: str
    url: str
    category: str
    description: str
    toc: str
    highlights: str
    methodology: str
    meta_title: str
    meta_desc: str
    meta_keyword: str
    pages: str
    created_date: str


class ReportListSchema(BaseModel):
    id: int
    url: str
    category: str


@router.get("/reports")
async def get_reports(db: Session = Depends(get_db)):
    reports = (
        db.query(Report).with_entities(Report.id, Report.url, Report.category).all()
    )
    report_list = [
        ReportListSchema(id=report.id, url=report.url, category=report.category)
        for report in reports
    ]
    return {"data": report_list}


@router.get("/reports/{report_id}")
async def get_report_by_id(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    return {"data": report}


@router.get("/reports/category/{category}")
async def get_reports_by_category(
    category: str,
    page: int,
    per_page: int,
    db: Session = Depends(get_db),
):
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    # Calculate the offset to skip records based on the page and per_page values
    offset = (page - 1) * per_page

    reports = (
        db.query(Report)
        .filter(Report.category == category)
        .offset(offset)
        .limit(per_page)
        .all()
    )
    
    report_list = [
        ReportListSchema(id=report.id, url=report.url, category=report.category)
        for report in reports
    ]

    return {"data": report_list}


@router.post("/reports")
async def create_report(report: CreateReportRequest, db: Session = Depends(get_db)):
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return {"data": db_report}


@router.put("/reports/{report_id}")
async def update_report(new_report: UpdateReportRequest, db: Session = Depends(get_db)):
    existing_report = db.query(Report).filter(Report.id == new_report.id).first()
    if existing_report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    for attr, value in new_report.dict().items():
        setattr(existing_report, attr, value)

    db.commit()
    db.refresh(existing_report)
    return {"data": existing_report}


@router.delete("/reports/{report_id}")
async def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
    return {"message": "Report deleted"}


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        file_extension = file.filename.split(".")[-1]

        destination_folder = "images"
        os.makedirs(destination_folder, exist_ok=True)

        file_path = os.path.join(destination_folder, f"{timestamp}.{file_extension}")

        contents = file.file.read()

        image = Image.open(io.BytesIO(contents))

        max_width = 800
        image.thumbnail((max_width, max_width))

        image.save(file_path)

    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {
        "message": f"Successfully uploaded and compressed {file.filename} to {file_path}"
    }
