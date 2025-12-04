from pydantic import BaseModel, Field, field_validator

class JournalEntry(BaseModel):
    user_id: str = Field(..., description="The ID of the user")
    title: str = Field(..., description="The title of the journal entry")
    thoughts: str = Field(..., description="The content/thoughts of the journal entry")

    @field_validator('user_id', 'title', 'thoughts')
    @classmethod
    def check_not_empty(cls, v, info):
        if not v or not v.strip():
            raise ValueError(f"You can't leave blank in '{info.field_name}' field")
        return v

class JournalEntryResponse(BaseModel):
    success: bool
    msg: str
