from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Git Changes!", "message": "Checking do git changes work!"}