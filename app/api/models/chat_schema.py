from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the user")
    message: str = Field(..., min_length=1, description="The current message from the user")
    session_id: Optional[str] = Field(None, description="The session ID to continue an existing conversation")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The response from the assistant")
