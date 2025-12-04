from fastapi import FastAPI
from app.api.endpoints import chat, insert_journal, insert_affirmation
from dotenv import load_dotenv
from app.middleware.setup import setup_middleware

load_dotenv()

app = FastAPI()

setup_middleware(app)

app.include_router(insert_journal.router, prefix="/api/v1", tags=["Journal"])
app.include_router(insert_affirmation.router, prefix="/api/v1", tags=["Affirmation"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Well-being API"}
