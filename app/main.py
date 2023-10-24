from fastapi import Depends, FastAPI, HTTPException
from mailjet_rest import Client
from dotenv import load_dotenv
from requests import Session
from . import models
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
load_dotenv()
from app.routers import email, report


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"greeting": "Hello!", "message": "This api works!"}

@app.get("/reports")
async def getReports(db: Session = Depends(get_db)):
    return {"status": "success"}

app.include_router(report.router)
app.include_router(email.router)
