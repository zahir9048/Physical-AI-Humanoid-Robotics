# Data Model: RAG Chatbot for Physical AI & Humanoid Robotics Textbook

## Entity: Conversation
**Description**: Represents a single user session with the chatbot
**Fields**:
- `id`: UUID (primary key) - Unique identifier for the conversation
- `created_at`: DateTime (default: now) - Timestamp when conversation started
- `expires_at`: DateTime - When the conversation session expires (for anonymous sessions)

**Relationships**:
- One-to-many with Message (conversation has many messages)

## Entity: Message
**Description**: Represents a single message in a conversation
**Fields**:
- `id`: UUID (primary key) - Unique identifier for the message
- `conversation_id`: UUID (foreign key) - Links to the conversation
- `role`: String (enum: 'user', 'assistant', 'system') - The sender type
- `content`: Text - The message content
- `timestamp`: DateTime (default: now) - When the message was created
- `source_chunks`: JSON (optional) - Array of source chunk IDs used to generate the response

**Relationships**:
- Many-to-one with Conversation (message belongs to one conversation)
- One-to-many with Feedback (message can have feedback)

## Entity: Feedback
**Description**: User feedback on chatbot responses
**Fields**:
- `id`: UUID (primary key) - Unique identifier for the feedback
- `message_id`: UUID (foreign key) - Links to the message being rated
- `rating`: Integer (range: -1 to 1) - Like (1), Dislike (-1), or Neutral (0)
- `comment`: Text (optional) - Additional feedback from user
- `timestamp`: DateTime (default: now) - When feedback was submitted

**Relationships**:
- Many-to-one with Message (feedback belongs to one message)

## Entity: TextbookChunk (Vector Database)
**Description**: Represents a chunk of textbook content stored in Qdrant
**Fields**:
- `id`: UUID - Unique identifier for the chunk
- `content`: Text - The actual content of the chunk
- `title`: String - Title of the section/chapter
- `chapter`: String - Chapter identifier
- `section`: String - Section identifier
- `url`: String - URL to the original page in the textbook
- `source_file`: String - Original MDX file name
- `position`: Integer - Position in the original document
- `metadata`: JSON - Additional metadata for retrieval

**Validation Rules**:
- Content must be between 100 and 1500 tokens
- Chapter and section must not be empty
- URL must be a valid relative path

## Entity: ChatQuery
**Description**: Represents a query made by the user (for analytics)
**Fields**:
- `id`: UUID (primary key) - Unique identifier for the query
- `conversation_id`: UUID (foreign key) - Links to the conversation
- `query_text`: Text - The original user query
- `selected_text`: Text (optional) - Text selected by user when making query
- `query_timestamp`: DateTime (default: now) - When query was made
- `response_time_ms`: Integer - Time taken to generate response
- `retrieved_chunks_count`: Integer - Number of chunks retrieved for the response
- `was_helpful`: Boolean (optional) - Whether the user found the response helpful

**Relationships**:
- Many-to-one with Conversation (query belongs to one conversation)

## State Transitions

### Conversation State Transitions
- Active → Expired (when session times out)
- Active → Cleared (when user manually clears history)

### Message State Transitions
- None (messages are immutable once created)

## Constraints

### Primary Keys
- All entities use UUIDs as primary keys for global uniqueness

### Foreign Key Constraints
- Message.conversation_id → Conversation.id (cascade delete)
- Feedback.message_id → Message.id (cascade delete)
- ChatQuery.conversation_id → Conversation.id (cascade delete)

### Validation Constraints
- Message.role must be one of 'user', 'assistant', 'system'
- Feedback.rating must be between -1 and 1
- Conversation.expires_at must be in the future
- TextbookChunk.content length must be appropriate for embedding model limits