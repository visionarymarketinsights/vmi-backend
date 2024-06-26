from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import FastAPI, APIRouter, HTTPException, Request
import os
import requests

from pydantic import BaseModel


from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from ..utils.rate_limit import limiter

from fastapi import BackgroundTasks

smtp_pass = os.environ["CONGSMTP"]
recaptcha_secret = os.environ["RECAPTCHA_SECRET_KEY"]


class EmailRequest(BaseModel):
    client_email: str
    client_content: str
    subject: str
    admin_content: str
    response_token: str
class RecaptchaResponse(BaseModel):
    success: bool
    message: str


router = APIRouter()


@router.get("/check_email")
@limiter.limit("5/minute")
def email_check(request: Request):
    return {'ip':request.client.host}

@router.post("/email")
async def email(email_request: EmailRequest, background_tasks: BackgroundTasks):
    try:
        if not email_request.response_token:
            return RecaptchaResponse(success=False, message='reCAPTCHA not completed.')

        verification_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': recaptcha_secret,
            'response': email_request.response_token,
        }
        response = requests.post(verification_url, data=payload)

        if response.json()['success']:
            background_tasks.add_task(send_email_in_background, email_request, is_client = True)
            background_tasks.add_task(send_email_in_background, email_request, is_client = False)
            return {"message": "Email sent successfully"}
        else:
            return RecaptchaResponse(success=False, message='reCAPTCHA verification failed.')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def send_email_in_background(email_request: EmailRequest, is_client: bool):
    msg = MIMEMultipart()
    msg["From"] = "support@visionarymarketinsights.com"
    msg["Subject"] = email_request.subject
    
    if is_client == True:
        msg["To"] = email_request.client_email
        recipients = [email_request.client_email]
        html_message = email_request.client_content
    else:
        msg["To"] = "support@visionarymarketinsights.com"
        recipients = ["support@visionarymarketinsights.com"]
        html_message = email_request.admin_content

    msg.attach(MIMEText(html_message, "html"))

    # Create an SMTP server connection
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login("support@visionarymarketinsights.com", smtp_pass)
        server.sendmail(
            "support@visionarymarketinsights.com", recipients, msg.as_string()
        )