from fastapi import FastAPI, HTTPException
from mailjet_rest import Client
from dotenv import load_dotenv

load_dotenv()

from app.routers import email, report


app = FastAPI()


@app.get("/")
async def root():
    return {"greeting": "Hello!", "message": "This api works!"}

app.include_router(report.router)
app.include_router(email.router)
