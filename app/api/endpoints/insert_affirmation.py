from fastapi import APIRouter, HTTPException
from app.api.models.insert_affirmation_schema import AffirmationEntry, AffirmationEntryResponse
from app.service.ingestion_pipeline.ingestion import insert_affirmation_into_pinecone

router = APIRouter()

@router.post("/insert_affirmation", response_model=AffirmationEntryResponse)
async def insert_affirmation(entry: AffirmationEntry):
    try:
        result = insert_affirmation_into_pinecone(entry.user_id, entry.daily_affirmation)
        return AffirmationEntryResponse(success=True, msg=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
