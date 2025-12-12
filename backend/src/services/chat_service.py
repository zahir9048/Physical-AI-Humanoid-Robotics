import openai
import cohere
import httpx
import re
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

    def _is_greeting(self, query: str) -> bool:
        """Check if the query is a simple greeting"""
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings']
        query_lower = query.lower().strip()
        return query_lower in greetings or query_lower in [g + '!' for g in greetings] or query_lower in [g + '.' for g in greetings]

    def _extract_module_week(self, chunk) -> str:
        """Extract module/week identifier from chunk"""
        # Try to extract from chapter field (e.g., "module-1" or "module-1/week-1")
        if chunk.chapter and 'module' in chunk.chapter.lower():
            # Extract module number
            module_match = re.search(r'module[-\s]?(\d+)', chunk.chapter.lower())
            week_match = re.search(r'week[-\s]?(\d+)', chunk.chapter.lower())
            
            if module_match:
                module_num = module_match.group(1)
                if week_match:
                    week_num = week_match.group(1)
                    return f"Module {module_num}, Week {week_num}"
                return f"Module {module_num}"
        
        # Try to extract from URL
        if chunk.url:
            module_match = re.search(r'module[-\s]?(\d+)', chunk.url.lower())
            week_match = re.search(r'week[-\s]?(\d+)', chunk.url.lower())
            
            if module_match:
                module_num = module_match.group(1)
                if week_match:
                    week_num = week_match.group(1)
                    return f"Module {module_num}, Week {week_num}"
                return f"Module {module_num}"
        
        # Fallback to chapter if it exists
        return chunk.chapter if chunk.chapter else "Unknown"

    async def _get_sample_keywords(self) -> List[str]:
        """Get sample keywords/topics from the textbook to suggest to users"""
        keywords = set()
        
        # Query for some general topics to extract keywords
        sample_queries = ["ROS 2", "introduction", "fundamentals", "robotics", "humanoid"]
        
        for query in sample_queries[:3]:  # Use first 3 queries
            try:
                chunks = await self.qdrant_service.search_chunks(query=query, top_k=2)
                for chunk in chunks:
                    # Extract keywords from title
                    if chunk.title:
                        # Clean title and extract meaningful terms
                        title = chunk.title.strip()
                        # Remove common words and extract key phrases
                        if len(title) > 3 and title not in ["Introduction", "Intro"]:
                            keywords.add(title)
                    
                    # Extract from section if it's meaningful
                    if chunk.section and chunk.section != "Intro" and len(chunk.section) > 3:
                        section = chunk.section.strip()
                        # Only add if it looks like a topic (not too long, has capital letters)
                        if len(section) < 50 and any(c.isupper() for c in section):
                            keywords.add(section)
            except Exception as e:
                print(f"Error getting sample keywords: {e}")
                continue
        
        # If we didn't get enough keywords, add some common ones from the textbook
        if len(keywords) < 3:
            common_keywords = ["ROS 2", "Physical AI", "Humanoid Robotics", "Nodes", "Topics", "Services", "Actions", "Publishers", "Subscribers"]
            keywords.update(common_keywords)
        
        # Return up to 5 keywords, prioritizing shorter, more specific ones
        keywords_list = list(keywords)
        # Sort by length (shorter first) and take up to 5
        keywords_list.sort(key=len)
        return keywords_list[:5]

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

        # Handle greetings with a simple response
        if self._is_greeting(query):
            greeting_response = "Hello! How can I help you with the Physical AI & Humanoid Robotics textbook?"
            await self.postgres_service.save_message(
                conversation_id=conversation_id,
                role="assistant",
                content=greeting_response,
                source_chunks=[]
            )
            return ChatResponse(
                response_text=greeting_response,
                citations=[],
                source_chunks=[]
            )

        # Retrieve relevant context from textbook content (already filtered by similarity)
        relevant_chunks = await self.retrieval_service.retrieve_relevant_chunks(query, selected_text)

        # If no relevant chunks found, return a no-match response with suggestions
        if not relevant_chunks or len(relevant_chunks) == 0:
            # Get sample keywords to suggest
            sample_keywords = await self._get_sample_keywords()
            if sample_keywords:
                keywords_str = ", ".join(sample_keywords)
                no_match_response = f"I can't find anything related to '{query}' in the textbook. You can search for: {keywords_str}."
            else:
                no_match_response = f"I can't find anything related to '{query}' in the textbook."
            
            await self.postgres_service.save_message(
                conversation_id=conversation_id,
                role="assistant",
                content=no_match_response,
                source_chunks=[]
            )
            return ChatResponse(
                response_text=no_match_response,
                citations=[],
                source_chunks=[]
            )

        # Build context for the LLM
        context_text = "\n\n".join([chunk.content for chunk in relevant_chunks])

        # Prepare citations
        citations = [Citation(
            title=chunk.title,
            url=chunk.url,
            chapter=chunk.chapter,
            section=chunk.section
        ) for chunk in relevant_chunks]

        # Create concise system prompt
        system_prompt = f"""You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer the user's question concisely using only the provided context. Keep responses brief and to the point.

Context: {context_text}"""

        # Include selected text if provided
        if selected_text:
            system_prompt += f"\n\nUser selected text: {selected_text}"

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

        # Extract meaningful source identifiers (module/week) instead of UUIDs
        source_identifiers = [self._extract_module_week(chunk) for chunk in relevant_chunks]
        # Remove duplicates while preserving order
        seen = set()
        unique_sources = []
        for src in source_identifiers:
            if src not in seen:
                seen.add(src)
                unique_sources.append(src)

        # Save assistant message
        await self.postgres_service.save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_response,
            source_chunks=[chunk.id for chunk in relevant_chunks]
        )

        return ChatResponse(
            response_text=assistant_response,
            citations=citations,
            source_chunks=unique_sources
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

        # Handle greetings with a simple response
        if self._is_greeting(query):
            greeting_response = "Hello! How can I help you with the Physical AI & Humanoid Robotics textbook?"
            for char in greeting_response:
                yield char
            await self.postgres_service.save_message(
                conversation_id=conversation_id,
                role="assistant",
                content=greeting_response,
                source_chunks=[]
            )
            return

        # Retrieve relevant context from textbook content
        retrieved_chunks = await self.retrieval_service.retrieve_relevant_chunks(query, selected_text)

        # If no relevant chunks found, return a no-match response with suggestions
        if not retrieved_chunks or len(retrieved_chunks) == 0:
            # Get sample keywords to suggest
            sample_keywords = await self._get_sample_keywords()
            if sample_keywords:
                keywords_str = ", ".join(sample_keywords)
                no_match_response = f"I can't find anything related to '{query}' in the textbook. You can search for: {keywords_str}."
            else:
                no_match_response = f"I can't find anything related to '{query}' in the textbook."
            
            for char in no_match_response:
                yield char
            await self.postgres_service.save_message(
                conversation_id=conversation_id,
                role="assistant",
                content=no_match_response,
                source_chunks=[]
            )
            return

        # Build context for the LLM
        context_text = "\n\n".join([chunk.content for chunk in retrieved_chunks])

        # Prepare citations
        citations = [Citation(
            title=chunk.title,
            url=chunk.url,
            chapter=chunk.chapter,
            section=chunk.section
        ) for chunk in retrieved_chunks]

        # Create concise system prompt
        system_prompt = f"""You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer the user's question concisely using only the provided context. Keep responses brief and to the point.

Context: {context_text}"""

        # Include selected text if provided
        if selected_text:
            system_prompt += f"\n\nUser selected text: {selected_text}"

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