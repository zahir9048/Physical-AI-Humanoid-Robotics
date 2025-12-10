from pydantic import BaseModel, Field
from typing import Optional

class FeedbackRequest(BaseModel):
    message_id: str = Field(..., description="ID of the message being rated", example="123e4567-e89b-12d3-a456-426614174001")
    rating: int = Field(..., ge=-1, le=1, description="Rating (-1: dislike, 0: neutral, 1: like)", example=1)
    comment: Optional[str] = Field(None, description="Optional comment with the feedback", example="This explanation was very helpful")

class FeedbackResponse(BaseModel):
    success: bool = Field(..., description="Whether feedback was submitted successfully", example=True)
    message: str = Field(..., description="Response message", example="Feedback submitted successfully")