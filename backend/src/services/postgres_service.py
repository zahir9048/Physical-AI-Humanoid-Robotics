from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime
from src.models.conversation import Conversation
from src.models.message import Message as MessageModel

class PostgresService:
    def __init__(self, db: Session):
        self.db = db

    async def get_or_create_conversation(self, conversation_id: str) -> Conversation:
        """
        Get existing conversation or create a new one
        """
        # Try to get existing conversation
        conversation = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

        if not conversation:
            # Create new conversation
            conversation = Conversation(
                id=conversation_id,
                expires_at=datetime.utcnow().replace(hour=23, minute=59, second=59)  # Expires at end of day
            )
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)

        return conversation

    async def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        source_chunks: Optional[List[str]] = None
    ) -> MessageModel:
        """
        Save a message to the database
        """
        message = MessageModel(
            conversation_id=conversation_id,
            role=role,
            content=content,
            source_chunks=str(source_chunks) if source_chunks else None
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    async def get_messages_for_conversation(self, conversation_id: str) -> List[MessageModel]:
        """
        Get all messages for a specific conversation
        """
        messages = self.db.query(MessageModel).filter(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.timestamp).all()

        return messages