from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from . import models
from .database import engine,  get_db
from app.routers import email, report

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"greeting": "Hello!", "message": "This api works!"}


app.include_router(report.router)
app.include_router(email.router)
