# Tasks: RAG Agent Service: OpenAI Agents SDK with Retrieval

**Input**: Design documents from `/specs/001-rag-agent-retrieval/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/api.yaml, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths shown below assume `backend/` directory at repository root as per `plan.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the FastAPI service.

- [x] T001 Create `backend/app/` directory structure: `backend/app/__init__.py`, `backend/app/main.py`, `backend/app/models.py`, `backend/app/services/__init__.py`, `backend/app/services/agent.py`, `backend/app/services/tools.py`, `backend/app/core/__init__.py`, `backend/app/core/config.py`.
- [x] T002 Create `backend/tests/` directory structure: `backend/tests/__init__.py`, `backend/tests/test_agent.py`, `backend/tests/test_api.py`.
- [x] T003 Update `backend/requirements.txt` with new dependencies: `fastapi`, `uvicorn`, `openai`, `pydantic`, `python-dotenv`, `qdrant-client`, `cohere`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented
**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement `backend/app/core/config.py` for loading environment variables (OPENAI_API_KEY, QDRANT_HOST, QDRANT_API_KEY, COHERE_API_KEY) and managing application settings.
- [x] T005 Define Pydantic models for `AgentQuery` and `AgentResponse` in `backend/app/models.py` based on `data-model.md` and `contracts/api.yaml`.
- [x] T006 Initialize FastAPI app instance in `backend/app/main.py`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Question Answering with Retrieval (P1) 🎯 MVP

**Goal**: AI agent answers questions accurately by using relevant information retrieved from the Qdrant vector database.

**Independent Test**: Send a question about the book content to the FastAPI `/chat` endpoint. Verify that the agent uses its retrieval tool (logging can confirm this) and provides an answer that is accurate and directly supported by the retrieved content.

### Implementation for User Story 1

- [x] T007 [US1] Implement the retrieval tool logic in `backend/app/services/tools.py`. This tool should wrap the functionality from `backend/retriever.py` to make it usable by the OpenAI Agent, accepting a natural language query and returning relevant chunks.
- [x] T008 [US1] Implement the OpenAI Agent in `backend/app/services/agent.py`. This involves initializing the agent, configuring it to use the retrieval tool defined in `tools.py`, and defining its basic behavior for question answering.
- [x] T009 [US1] Create the `/chat` POST endpoint in `backend/app/main.py`. This endpoint should accept an `AgentQuery` (Pydantic model) as input, orchestrate the agent's invocation with the query, and return an `AgentResponse` (Pydantic model).
- [x] T010 [US1] Add basic logging and error handling for the `/chat` endpoint and agent invocation, ensuring errors from downstream services (Qdrant, OpenAI, Cohere) are caught and logged gracefully.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Context-Limited Question Answering (P2)

**Goal**: AI agent focuses its answer on a specific text provided by the user.

**Independent Test**: Send a question along with a `context_snippet` to the FastAPI `/chat` endpoint. Verify that the agent's answer is derived solely from the provided `context_snippet` and does not consult the retrieval tool for general search if a context is given.

### Implementation for User Story 2

- [x] T011 [US2] Modify the agent logic in `backend/app/services/agent.py` to check for a provided `context_snippet` in the `AgentQuery`. If present, the agent should prioritize using this context for answering before resorting to its general retrieval tool.
- [x] T012 [US2] Ensure the `/chat` endpoint in `backend/app/main.py` correctly handles and passes the optional `context_snippet` from the incoming request to the agent.

**Checkpoint**: All user stories should now be independently functional

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple components or the overall pipeline

- [x] T013 Implement FastAPI exception handlers for external API calls (Qdrant, OpenAI, Cohere) as per NFR-004, providing consistent error responses and detailed logging.
- [x] T014 Implement response latency measurement (SC-002) for the `/chat` endpoint in `backend/app/main.py`, logging the p95 response time.
- [x] T015 Add unit tests for `backend/app/services/agent.py` logic in `backend/tests/test_agent.py`, focusing on tool invocation and context handling.
- [x] T016 Add integration tests for the `/chat` endpoint in `backend/app/main.py` in `backend/tests/test_api.py`, ensuring correct API behavior and agent responses.
- [x] T017 Update `backend/quickstart.md` with detailed instructions for running the FastAPI service (`uvicorn`) and testing the API endpoints using `curl` examples for both general and context-limited queries.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion.
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion (specifically the agent and API endpoint).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P2)**: Depends on User Story 1 (`backend/app/services/agent.py`, `/chat` endpoint).

### Within Each User Story

- Tasks are generally sequential, building functionality step-by-step.
- Tool implementation before agent integration.
- Agent implementation before endpoint creation.
- CLI/API endpoint creation tasks should be done after core functionality is implemented.

### Parallel Opportunities

- Tasks T001 and T002 (creating directory structures) can be done in parallel.
- Once Foundational tasks (T004-T006) are complete, aspects of User Story 1 (e.g., retrieval tool implementation) and User Story 2 (e.g., initial agent setup if not tightly coupled) could potentially be worked on in parallel, though sequential is safer for dependencies.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (core agent and retrieval via API)
4. **STOP and VALIDATE**: Test the `/chat` endpoint with various queries to ensure correct agent behavior and retrieval grounding.

### Incremental Delivery

1. Complete Setup + Foundational → Basic FastAPI app ready.
2. Add User Story 1 → Core RAG agent functional → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Context-limited queries handled → Test independently → Deploy/Demo.
4. Complete Polish Phase for robustness, performance, and documentation.

---

## Notes

- All tasks are designed for implementation within `backend/` directory, following the `backend/app` structure.
- Each user story should be independently completable and testable.
- Verify API endpoint behavior and agent responses after each major task.
- Commit after each task or logical group.
- Stop at any checkpoint to validate story independently.
