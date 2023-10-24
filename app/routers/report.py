from fastapi import Depends,   APIRouter, HTTPException
from pydantic import BaseModel
from app import models

from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()



# Pydantic Models
class CreateReportRequest(BaseModel):
    title: str
    report_description: str

class UpdateReportRequest(BaseModel):
    title: str
    report_description: str

class ReportResponse(BaseModel):
    id: int
    title: str
    report_description: str


@router.get("/reports")
async def get_reports(db: Session = Depends(get_db)):
    reports = db.query(models.Report).all()
    return {"data": reports}

@router.post("/reports")
async def create_report(report: CreateReportRequest, db: Session = Depends(get_db)):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return {"data": db_report}

@router.put("/reports/{report_id}")
async def update_report(report_id: int, new_report: UpdateReportRequest, db: Session = Depends(get_db)):
    existing_report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if existing_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    for attr, value in new_report.dict().items():
        setattr(existing_report, attr, value)
    
    db.commit()
    db.refresh(existing_report)
    return {"data": existing_report}

@router.delete("/reports/{report_id}")
async def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    return {"message": "Report deleted"}
