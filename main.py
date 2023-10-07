from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Git Changes!", "message": "Checking do git changes work!"}

@app.get("/simple__http_call")
async def make_http_call():
    # Define the URL of the external API you want to call
    external_api_url = "http://firstjumpuatservice.express-engg.com/api/Attendance/GetServerTime"

    # Create an instance of the httpx.AsyncClient
    async with httpx.AsyncClient() as client:
        # Make an HTTP GET request to the external API
        response = await client.get(external_api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response from the external API
            data = response.json()
            return {"data_from_external_api": data}
        else:
            # Handle error cases here
            return {"error": "Failed to fetch data from the external API", "status_code": response.status_code}
