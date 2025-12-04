from pydantic import BaseModel, Field, field_validator

class AffirmationEntry(BaseModel):
    user_id: str = Field(..., description="The ID of the user")
    daily_affirmation: str = Field(..., description="The daily affirmation content")

    @field_validator('user_id', 'daily_affirmation')
    @classmethod
    def check_not_empty(cls, v, info):
        if not v or not v.strip():
            raise ValueError(f"You can't leave blank in '{info.field_name}' field")
        return v

class AffirmationEntryResponse(BaseModel):
    success: bool
    msg: str
