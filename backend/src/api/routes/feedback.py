from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import uuid
from src.core.database import get_db
from src.schemas.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter()

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback_request: FeedbackRequest, db: Session = Depends(get_db)):
    """
    Submit user feedback on a specific message
    """
    try:
        # Validate message ID format
        try:
            uuid.UUID(feedback_request.message_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message ID format"
            )

        # Validate rating range
        if feedback_request.rating not in [-1, 0, 1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be -1, 0, or 1"
            )

        # Save feedback to database
        from src.models.feedback import Feedback

        # Check if feedback already exists for this message?
        # For simplicity, we just add a new record. In a real app, might want to update.
        
        new_feedback = Feedback(
            message_id=feedback_request.message_id,
            rating=feedback_request.rating,
            comment=feedback_request.comment
        )
        
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)

        return FeedbackResponse(
            success=True,
            message="Feedback submitted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )