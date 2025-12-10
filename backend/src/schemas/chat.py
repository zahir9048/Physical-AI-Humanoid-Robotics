from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's question or query", example="Explain ROS 2 nodes")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for maintaining context", example="123e4567-e89b-12d3-a456-426614174000")
    selected_text: Optional[str] = Field(None, description="Optional text selected by the user for context", example="A ROS 2 node is a process that performs computation...")
    page_url: Optional[str] = Field(None, description="Optional URL of the page where query originated", example="/module-1/week-1")

class Citation(BaseModel):
    title: str = Field(..., description="Title of the cited section", example="Understanding ROS 2 Nodes")
    url: str = Field(..., description="URL to the cited section", example="/module-1/week-1#ros2-nodes")
    chapter: str = Field(..., description="Chapter identifier", example="Module 1, Week 1")
    section: str = Field(..., description="Section identifier", example="ROS 2 Architecture")

class ChatResponse(BaseModel):
    conversation_id: str = Field(..., description="The conversation ID", example="123e4567-e89b-12d3-a456-426614174000")
    response: str = Field(..., description="The chatbot's response", example="ROS 2 nodes are...")
    citations: List[Citation] = Field(..., description="List of citations to textbook sections")
    sources: List[str] = Field(default=[], description="List of source chunk IDs used in response")

class Message(BaseModel):
    id: str
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: str

class ConversationHistory(BaseModel):
    conversation_id: str
    messages: List[Message]