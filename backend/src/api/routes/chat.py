from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from src.core.database import get_db
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.chat_service import ChatService

router = APIRouter()

@router.post("/chat/query", response_model=ChatResponse)
async def chat_query(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process a chat query and return a response
    """
    try:
        # Validate input
        if not chat_request.query or len(chat_request.query.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )

        if len(chat_request.query) > 1000:  # From config
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query too long"
            )

        # Generate conversation ID if not provided
        conversation_id = chat_request.conversation_id or str(uuid.uuid4())

        # Initialize chat service and process the query
        chat_service = ChatService(db)
        response = await chat_service.process_query(
            query=chat_request.query,
            conversation_id=conversation_id,
            selected_text=chat_request.selected_text,
            page_url=chat_request.page_url
        )

        return ChatResponse(
            conversation_id=conversation_id,
            response=response.response_text,
            citations=response.citations,
            sources=response.source_chunks or []
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/chat/stream")
async def chat_stream(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """
    Stream chat response using Server-Sent Events
    """
    try:
        # Validate input
        if not chat_request.query or len(chat_request.query.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )

        # Generate conversation ID if not provided
        conversation_id = chat_request.conversation_id or str(uuid.uuid4())

        # Initialize chat service and stream the response
        chat_service = ChatService(db)

        # Return a streaming response
        async def generate():
            async for token in chat_service.stream_response(
                query=chat_request.query,
                conversation_id=conversation_id,
                selected_text=chat_request.selected_text,
                page_url=chat_request.page_url
            ):
                yield f"data: {token}\n\n"

        return generate()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )