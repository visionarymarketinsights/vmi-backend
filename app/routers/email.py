from fastapi import FastAPI,  APIRouter
from mailjet_rest import Client
import os

api_key = os.environ["MJ_APIKEY_PUBLIC"]
api_secret = os.environ["MJ_APIKEY_PRIVATE"]

mailjet = Client(auth=(api_key, api_secret), version="v3.1")

router = APIRouter()

@router.get("/email")
async def email(subject: str, content: str):
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
                "Subject": subject,
                "HTMLPart": content,
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    return result.json()
