from fastapi import FastAPI
from app.api.endpoints import chat
from dotenv import load_dotenv
from app.middleware.setup import setup_middleware

load_dotenv()

app = FastAPI()

setup_middleware(app)

app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Well-being API"}
