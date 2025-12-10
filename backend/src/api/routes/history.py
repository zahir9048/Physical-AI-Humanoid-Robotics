from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from src.core.database import get_db
from src.schemas.chat import ConversationHistory
from src.services.chat_service import ChatService

router = APIRouter()

@router.get("/chat/history/{conversation_id}", response_model=ConversationHistory)
async def get_conversation_history(conversation_id: str, db: Session = Depends(get_db)):
    """
    Retrieve the history of messages for a specific conversation
    """
    try:
        # Validate conversation ID format
        try:
            uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )

        chat_service = ChatService(db)
        history = await chat_service.get_conversation_history(conversation_id)

        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        return history
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )