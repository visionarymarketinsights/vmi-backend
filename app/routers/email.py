from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import FastAPI,  APIRouter, HTTPException, Request
import os

from pydantic import BaseModel


from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from ..utils.rate_limit import limiter

smtp_pass = os.environ["SIDSMTP"]


class EmailRequest(BaseModel):
    subject: str
    content: str

router = APIRouter()

@router.post("/email")
@limiter.limit("5/minute")
async def email(request: Request, email_request: EmailRequest):
    try:
        # Create a message
        msg = MIMEMultipart()
        msg["From"] = 'Siddhant <siddhant.pandagle1998@gmail.com>'
        msg["To"] = 'siddhant.pandagle1998@gmail.com'
        msg["Subject"] = email_request.subject

        # Add the HTML message body
        html_message = email_request.content
        msg.attach(MIMEText(html_message, "html"))

        # Create an SMTP server connection
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login('siddhant.pandagle1998', smtp_pass)
            server.sendmail('Siddhant', 'siddhant.pandagle1998@gmail.com', msg.as_string())

        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
