from fastapi import FastAPI, HTTPException
from mailjet_rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

app = FastAPI()


@app.get("/")
async def root():
    return {"greeting": "Hello!", "message": "This api works!"}


@app.get("/send_email")
async def send_email(subject:str, content:str):
    data = {
        'Messages': 
        [
            {
            "From": {
                "Email": "siddhant.pandagle1998@gmail.com",
                "Name": "Siddhant Pandagle"
            },
            "To": [
                {
                "Email": "siddhant.pandagle1998@gmail.com",
                "Name": "Siddhant Pandagle"
                }
            ],
            "Subject": subject,
            # "TextPart": "Greetings from Siddhant Pandagle!",
            "HTMLPart": content
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    return result.json()