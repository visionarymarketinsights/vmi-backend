# Import necessary modules and dependencies
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Report  # Import the Report model
from app.database import get_db
from sqlalchemy import func

router = APIRouter()

# Pydantic Models
class CreateReportRequest(BaseModel):
    title: str
    url: str  # Include the new 'url' field
    category: str  # Include the new 'category' field
    description: str  # Include the new 'description' field
    toc: str  # Include the new 'toc' field
    highlights: str  # Include the new 'highlights' field
    methodology: str  # Include the new 'methodology' field
    meta_title: str  # Include the new 'meta_title' field
    meta_desc: str  # Include the new 'meta_desc' field
    meta_keyword: str  # Include the new 'meta_keyword' field

class UpdateReportRequest(BaseModel):
    title: str
    url: str  # Include the new 'url' field
    category: str  # Include the new 'category' field
    description: str  # Include the new 'description' field
    toc: str  # Include the new 'toc' field
    highlights: str  # Include the new 'highlights' field
    methodology: str  # Include the new 'methodology' field
    meta_title: str  # Include the new 'meta_title' field
    meta_desc: str  # Include the new 'meta_desc' field
    meta_keyword: str  # Include the new 'meta_keyword' field

class ReportResponse(BaseModel):
    id: int
    title: str
    url: str  # Include the new 'url' field
    category: str  # Include the new 'category' field
    description: str  # Include the new 'description' field

# Update the API routes
@router.get("/reports")
async def get_reports(db: Session = Depends(get_db)):
    reports = db.query(Report).all()
    return {"data": reports}

@router.post("/reports")
async def create_report(report: CreateReportRequest, db: Session = Depends(get_db)):
    db_report = Report(**report.dict(), created_date=func.now())  # Set 'created_date' using func.now()
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return {"data": db_report}

@router.put("/reports/{report_id}")
async def update_report(report_id: int, new_report: UpdateReportRequest, db: Session = Depends(get_db)):
    existing_report = db.query(Report).filter(Report.id == report_id).first()
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
