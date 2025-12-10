---
description: "Task list for RAG Chatbot implementation"
---

# Tasks: RAG Chatbot for Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/002-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure in backend/ with FastAPI dependencies
- [X] T002 Create frontend project structure in frontend/ with React dependencies
- [X] T003 [P] Configure linting and formatting tools for Python (backend)
- [X] T004 [P] Configure linting and formatting tools for TypeScript/React (frontend)
- [X] T005 [P] Create initial requirements.txt for backend with FastAPI, OpenAI, Qdrant, Pydantic
- [X] T006 [P] Create initial package.json for frontend with React, TypeScript, Tailwind CSS

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Setup database schema and migrations framework for Neon Postgres
- [X] T008 [P] Implement configuration management with python-dotenv in backend/src/core/config.py
- [X] T009 [P] Setup API routing and middleware structure in backend/src/api/main.py
- [X] T010 Create base models/entities that all stories depend on in backend/src/models/
- [X] T011 Configure error handling and logging infrastructure in backend/src/core/
- [X] T012 Setup CORS middleware for Docusaurus integration in backend/src/api/main.py
- [X] T013 [P] Setup Qdrant vector database connection in backend/src/core/database.py
- [X] T014 [P] Setup Postgres database connection in backend/src/core/database.py
- [X] T015 Create embedding service in backend/src/services/embedding_service.py
- [X] T016 Create text splitter utility in backend/src/utils/text_splitter.py
- [X] T017 Create basic frontend services in frontend/src/services/ChatAPI.ts
- [X] T018 Create frontend types in frontend/src/services/types.ts
- [X] T019 Create setup scripts for Qdrant and Postgres in scripts/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Q&A with Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable students to ask questions about book content and receive relevant answers with citations to specific chapters/sections

**Independent Test**: Can be fully tested by opening the chatbot, asking a question about book content, and receiving a relevant response with proper citations to specific sections of the book.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T020 [P] [US1] Contract test for /api/chat/query endpoint in backend/tests/contract/test_chat_api.py
- [ ] T021 [P] [US1] Integration test for basic Q&A user journey in backend/tests/integration/test_basic_qa.py

### Implementation for User Story 1

- [X] T022 [P] [US1] Create Conversation model in backend/src/models/conversation.py
- [X] T023 [P] [US1] Create Message model in backend/src/models/message.py
- [X] T024 [US1] Implement ChatService in backend/src/services/chat_service.py
- [X] T025 [US1] Implement RetrievalService in backend/src/services/retrieval_service.py
- [X] T026 [US1] Implement QdrantService in backend/src/services/qdrant_service.py
- [X] T027 [US1] Implement PostgresService in backend/src/services/postgres_service.py
- [X] T028 [US1] Create /api/chat/query endpoint in backend/src/api/routes/chat.py
- [X] T029 [US1] Create ChatWidget component in frontend/src/components/ChatWidget.tsx
- [X] T030 [US1] Create ChatMessage component in frontend/src/components/ChatMessage.tsx
- [X] T031 [US1] Create ChatInput component in frontend/src/components/ChatInput.tsx
- [X] T032 [US1] Implement basic chat API service in frontend/src/services/ChatAPI.ts
- [X] T033 [US1] Add streaming response handling with Server-Sent Events in frontend
- [X] T034 [US1] Add markdown rendering for responses in ChatMessage component
- [X] T035 [US1] Add citation display to responses in ChatMessage component
- [X] T036 [US1] Implement basic chat history persistence in browser storage
- [X] T037 [US1] Add loading states and skeleton loaders in UI
- [X] T038 [US1] Add error handling with user-friendly messages in frontend

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Text Selection Q&A (Priority: P2)

**Goal**: Enable students to select specific text on any page and ask targeted questions about that content to get focused explanations

**Independent Test**: Can be fully tested by selecting text on a page, opening the chatbot, and receiving a response that addresses the selected text specifically while potentially referencing related content.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T039 [P] [US2] Contract test for /api/chat/query with selected_text in backend/tests/contract/test_chat_api.py
- [ ] T040 [P] [US2] Integration test for text selection Q&A user journey in backend/tests/integration/test_text_selection.py

### Implementation for User Story 2

- [X] T041 [P] [US2] Create TextSelectionHandler component in frontend/src/components/TextSelectionHandler.tsx
- [X] T042 [US2] Implement text selection event listeners in TextSelectionHandler
- [ ] T043 [US2] Add floating "Ask AI" button that appears near selection
- [X] T044 [US2] Pass selected text and page URL to chatbot when button clicked
- [X] T045 [US2] Modify ChatService to handle selected text context in backend/src/services/chat_service.py
- [X] T046 [US2] Update /api/chat/query endpoint to accept and process selected_text in backend/src/api/routes/chat.py
- [X] T047 [US2] Modify RAG flow to prioritize selected text in context assembly
- [X] T048 [US2] Update frontend API service to send selected text with queries
- [X] T049 [US2] Update ChatWidget to handle pre-filled context from text selection

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Conversation History and Context (Priority: P3)

**Goal**: Enable students to maintain conversation history and have multi-turn conversations to ask follow-up questions without repeating context

**Independent Test**: Can be fully tested by having a multi-turn conversation where follow-up questions reference previous exchanges without requiring the user to restate context.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T050 [P] [US3] Contract test for /api/chat/history endpoint in backend/tests/contract/test_history_api.py
- [ ] T051 [P] [US3] Integration test for multi-turn conversation in backend/tests/integration/test_conversation_context.py

### Implementation for User Story 3

- [X] T052 [P] [US3] Create /api/chat/history/{conversation_id} endpoint in backend/src/api/routes/history.py
- [X] T053 [US3] Implement conversation history retrieval in backend/src/services/chat_service.py
- [X] T054 [US3] Implement conversation context management in backend/src/services/chat_service.py
- [X] T055 [US3] Add conversation persistence in PostgresService for multi-turn context
- [X] T056 [US3] Update ChatWidget to maintain conversation context in frontend
- [X] T057 [US3] Add clear conversation history functionality in frontend/src/components/ChatWidget.tsx
- [X] T058 [US3] Implement follow-up question context handling in frontend/src/hooks/useChat.ts
- [X] T059 [US3] Update frontend API service to handle conversation history requests
- [X] T060 [US3] Add UI controls for conversation history management

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Cross-cutting Features

**Goal**: Implement additional features that enhance all user stories

- [ ] T061 [P] Implement rate limiting with HTTP 429 status codes in backend middleware
- [ ] T062 [P] Implement caching for common queries in backend/src/services/chat_service.py
- [X] T063 [P] Add feedback functionality with Feedback model in backend/src/models/feedback.py
- [X] T064 Create /api/feedback endpoint in backend/src/api/routes/feedback.py
- [X] T065 Add feedback UI to ChatMessage component in frontend
- [ ] T066 Implement voice input support using Web Speech API in frontend/src/components/ChatInput.tsx
- [X] T067 Add code syntax highlighting in response rendering
- [X] T068 Create /api/health endpoint in backend/src/api/routes/health.py
- [ ] T069 Implement exponential backoff for OpenAI API calls in backend/src/services/chat_service.py
- [ ] T070 Add comprehensive logging for analytics in backend/src/core/

---

## Phase 7: Document Processing Pipeline

**Goal**: Set up the initial ingestion of textbook content into the vector database

- [X] T071 Create document parser for MDX/MD files in backend/src/utils/document_parser.py
- [X] T072 Implement document chunking by section structure in backend/src/utils/text_splitter.py
- [X] T073 Create embedding generation and storage in scripts/ingest_documents.py
- [X] T074 Add metadata extraction for textbook content in document parser
- [X] T075 Create initial data ingestion script to populate Qdrant in scripts/ingest_documents.py
- [X] T076 Test document processing with sample textbook content

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T077 [P] Documentation updates in docs/
- [X] T078 Code cleanup and refactoring
- [ ] T079 Performance optimization across all stories
- [X] T080 [P] Additional unit tests in backend/tests/unit/ and frontend/tests/unit/
- [ ] T081 Security hardening
- [X] T082 Run quickstart.md validation
- [X] T083 Deploy backend to Render or Railway
- [X] T084 Integrate frontend widget with Docusaurus site
- [X] T085 Test end-to-end functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Conversation model in backend/src/models/conversation.py"
Task: "Create Message model in backend/src/models/message.py"

# Launch all services for User Story 1 together:
Task: "Implement ChatService in backend/src/services/chat_service.py"
Task: "Implement RetrievalService in backend/src/services/retrieval_service.py"
Task: "Implement QdrantService in backend/src/services/qdrant_service.py"
Task: "Implement PostgresService in backend/src/services/postgres_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence