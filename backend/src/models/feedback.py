from sqlalchemy import Column, DateTime, String, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from src.core.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # -1, 0, or 1
    comment = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())