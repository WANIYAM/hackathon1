# Data Model: Frontend-Backend Integration for RAG Chatbot

This feature focuses on the integration between an existing Docusaurus frontend and a FastAPI RAG agent backend. As such, it does not introduce new core data models. The primary interaction involves sending text-based queries and receiving text-based responses.

Existing relevant data models (managed by the RAG backend, out of scope for this feature):
-   User queries and their associated context.
-   RAG agent's internal data structures for knowledge retrieval and generation.
