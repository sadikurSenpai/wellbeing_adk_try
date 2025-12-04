from fastapi import APIRouter, HTTPException
from app.api.models.insert_journal_schema import JournalEntry, JournalEntryResponse
from app.service.ingestion_pipeline.ingestion import insert_journal_into_pinecone

router = APIRouter()

@router.post("/insert_journal", response_model=JournalEntryResponse)
async def insert_journal(entry: JournalEntry):
    try:
        result = insert_journal_into_pinecone(entry.user_id, entry.title, entry.thoughts)
        return JournalEntryResponse(success=True, msg=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
