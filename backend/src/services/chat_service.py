import openai
import cohere
import httpx
from sqlalchemy.orm import Session
from typing import List, Optional, AsyncGenerator
import uuid
from datetime import datetime
from src.core.config import settings
from src.schemas.chat import Citation
from src.models.conversation import Conversation
from src.models.message import Message as MessageModel
from src.services.retrieval_service import RetrievalService
from src.services.qdrant_service import QdrantService
from src.services.postgres_service import PostgresService

class ChatResponse:
    def __init__(self, response_text: str, citations: List[Citation], source_chunks: Optional[List[str]] = None):
        self.response_text = response_text
        self.citations = citations
        self.source_chunks = source_chunks or []

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.provider = settings.LLM_PROVIDER

        if self.provider == "openai":
            self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.provider == "cohere":
            self.cohere_client = cohere.Client(api_key=settings.COHERE_API_KEY)
        # For ollama, we'll use HTTP requests directly

        self.retrieval_service = RetrievalService()
        self.qdrant_service = QdrantService()
        self.postgres_service = PostgresService(db)

    async def process_query(
        self,
        query: str,
        conversation_id: str,
        selected_text: Optional[str] = None,
        page_url: Optional[str] = None
    ) -> ChatResponse:
        """
        Process a chat query and return a response
        """
        # Create or get conversation
        conversation = await self.postgres_service.get_or_create_conversation(conversation_id)

        # Save user message
        await self.postgres_service.save_message(
            conversation_id=conversation_id,
            role="user",
            content=query
        )

        # Retrieve relevant context from textbook content
        retrieved_chunks = await self.retrieval_service.retrieve_relevant_chunks(query, selected_text)

        # Build context for the LLM
        context_text = "\n\n".join([chunk.content for chunk in retrieved_chunks])

        # Prepare citations
        citations = [Citation(
            title=chunk.title,
            url=chunk.url,
            chapter=chunk.chapter,
            section=chunk.section
        ) for chunk in retrieved_chunks]

        # Create the system prompt with context
        system_prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
        Use the following context to answer the user's question.
        If the context doesn't contain enough information to answer the question, say so.
        Always cite the relevant sections of the textbook in your response.

        Context: {context_text}
        """

        # Include selected text if provided
        if selected_text:
            system_prompt += f"\n\nThe user has selected this specific text: {selected_text}"

        # Get conversation history for context in multi-turn conversations
        # We'll fetch raw messages from Postgres to avoid schema conversion issues
        raw_messages = await self.postgres_service.get_messages_for_conversation(conversation_id)
        conversation_context = []
        if raw_messages:
            # Include last 5 messages for context (to avoid exceeding token limits)
            recent_messages = raw_messages[-5:]  # Get last 5 messages
            for msg in recent_messages:
                # Map role to Cohere expected format
                role = "CHATBOT" if msg.role == "assistant" else "USER"
                conversation_context.append({
                    "role": role,
                    "message": msg.content
                })

        # Get response based on provider
        if self.provider == "openai":
            # Prepare messages for OpenAI API
            openai_messages = [{"role": "system", "content": system_prompt}]
            openai_messages.extend(conversation_context)
            openai_messages.append({"role": "user", "content": query})

            # Get response from OpenAI
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=openai_messages,
                max_tokens=settings.MAX_RESPONSE_LENGTH
            )
            assistant_response = response.choices[0].message.content

        elif self.provider == "cohere":
            # Cohere format requires 'role' (USER/CHATBOT) and 'message' keys in chat_history

            # Get response from Cohere
            response = self.cohere_client.chat(
                message=f"{system_prompt}\n\n{query}",
                chat_history=conversation_context if conversation_context else None,
                max_tokens=settings.MAX_RESPONSE_LENGTH
            )
            assistant_response = response.text

        elif self.provider == "ollama":
            # Prepare messages for Ollama API (which mimics OpenAI)
            ollama_messages = [{"role": "system", "content": system_prompt}]
            ollama_messages.extend(conversation_context)
            ollama_messages.append({"role": "user", "content": query})

            # Get response from Ollama
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.OLLAMA_URL}/api/chat",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "messages": ollama_messages,
                        "stream": False,
                        "options": {"num_predict": settings.MAX_RESPONSE_LENGTH}
                    },
                    timeout=60.0
                )
                result = response.json()
                assistant_response = result["message"]["content"]

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        # Save assistant message
        await self.postgres_service.save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_response,
            source_chunks=[chunk.id for chunk in retrieved_chunks]
        )

        return ChatResponse(
            response_text=assistant_response,
            citations=citations,
            source_chunks=[chunk.id for chunk in retrieved_chunks]
        )

    async def stream_response(
        self,
        query: str,
        conversation_id: str,
        selected_text: Optional[str] = None,
        page_url: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat response using Server-Sent Events
        """
        # Create or get conversation
        conversation = await self.postgres_service.get_or_create_conversation(conversation_id)

        # Save user message
        await self.postgres_service.save_message(
            conversation_id=conversation_id,
            role="user",
            content=query
        )

        # Retrieve relevant context from textbook content
        retrieved_chunks = await self.retrieval_service.retrieve_relevant_chunks(query, selected_text)

        # Build context for the LLM
        context_text = "\n\n".join([chunk.content for chunk in retrieved_chunks])

        # Prepare citations
        citations = [Citation(
            title=chunk.title,
            url=chunk.url,
            chapter=chunk.chapter,
            section=chunk.section
        ) for chunk in retrieved_chunks]

        # Create the system prompt with context
        system_prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
        Use the following context to answer the user's question.
        If the context doesn't contain enough information to answer the question, say so.
        Always cite the relevant sections of the textbook in your response.

        Context: {context_text}
        """

        # Include selected text if provided
        if selected_text:
            system_prompt += f"\n\nThe user has selected this specific text: {selected_text}"

        # Stream response based on provider
        if self.provider == "openai":
            # Stream response from OpenAI
            stream = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=settings.MAX_RESPONSE_LENGTH,
                stream=True
            )

            full_response = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response += token
                    yield token

        elif self.provider == "cohere":
            # Cohere streaming
            response = self.cohere_client.chat_stream(
                message=f"{system_prompt}\n\n{query}",
                max_tokens=settings.MAX_RESPONSE_LENGTH
            )

            full_response = ""
            for event in response:
                if event.event_type == "text-generation":
                    token = event.text
                    full_response += token
                    yield token

        elif self.provider == "ollama":
            # Stream response from Ollama
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{settings.OLLAMA_URL}/api/chat",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": query}
                        ],
                        "stream": True,
                        "options": {"num_predict": settings.MAX_RESPONSE_LENGTH}
                    },
                    timeout=60.0
                ) as response:
                    full_response = ""
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                token = data["message"]["content"]
                                full_response += token
                                yield token

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        # Save assistant message after streaming is complete
        await self.postgres_service.save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_response,
            source_chunks=[chunk.id for chunk in retrieved_chunks]
        )

    async def get_conversation_history(self, conversation_id: str):
        """
        Retrieve the history of messages for a conversation
        """
        from src.schemas.chat import ConversationHistory, Message as MessageSchema

        # Get messages from database
        db_messages = await self.postgres_service.get_messages_for_conversation(conversation_id)

        if not db_messages:
            return None

        # Convert DB models to schema format
        messages = []
        for db_msg in db_messages:
            message = MessageSchema(
                id=str(db_msg.id),
                role=db_msg.role,
                content=db_msg.content,
                timestamp=db_msg.timestamp.isoformat() if db_msg.timestamp else "",
                source_chunks=db_msg.source_chunks
            )
            messages.append(message)
        print(messages)
        return ConversationHistory(
            conversation_id=conversation_id,
            messages=messages
        )