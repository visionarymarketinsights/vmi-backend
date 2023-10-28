from fastapi import FastAPI,  APIRouter
from mailjet_rest import Client
import os

from pydantic import BaseModel

api_key = os.environ["MJ_APIKEY_PUBLIC"]
api_secret = os.environ["MJ_APIKEY_PRIVATE"]

mailjet = Client(auth=(api_key, api_secret), version="v3.1")


class EmailRequest(BaseModel):
    subject: str
    content: str

router = APIRouter()

@router.post("/email")
async def email(email_request:EmailRequest):
    data = {
        "Messages": [
            {
                "From": {
                    "Email": "siddhant.pandagle1998@gmail.com",
                    "Name": "Siddhant Pandagle",
                },
                "To": [
                    {
                        "Email": "siddhant.pandagle1998@gmail.com",
                        "Name": "Siddhant Pandagle",
                    }
                ],
                "Subject": email_request.subject,
                "HTMLPart": email_request.content,
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    return result.json()
