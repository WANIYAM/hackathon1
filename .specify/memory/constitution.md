<!--
---
Sync Impact Report
---
- **Version change**: N/A → 1.0.0
- **Added Principles**:
  - I. Unified Content and Interaction Architecture
  - II. Strict Performance and Resource Efficiency
  - III. Uncompromising Quality and Accuracy
  - IV. Automated Development and Deployment
- **Templates Status**:
  - ✅ `.specify/templates/plan-template.md` (Aligned)
  - ✅ `.specify/templates/spec-template.md` (Aligned)
  - ✅ `.specify/templates/tasks-template.md` (Aligned)
- **Follow-up TODOs**:
  - TODO(Principles): Define principles for Observability, Versioning, and Simplicity (Principles V, VI).
-->

# AI/Spec-Driven Book + RAG Chatbot Constitution

## Core Principles

### I. Unified Content and Interaction Architecture
The project comprises two core components: a static content book built with Docusaurus, and an interactive RAG chatbot. The book's content is generated via a "Spec-Kit Plus → Claude Code" workflow. The chatbot is built using OpenAI Agents, FastAPI, Neon Postgres for storage, and Qdrant for vector search. This separation allows for specialized development while ensuring the chatbot is grounded in the book's content.

### II. Strict Performance and Resource Efficiency
All operations must be optimized for performance and cost. The chatbot MUST respond with a p95 latency of less than 3 seconds. The entire project MUST adhere to free-tier service limits, specifically Qdrant (1GB) and Neon Postgres (500MB). The repository size MUST remain under 500MB, and CI/CD build times MUST NOT exceed 2 minutes.

### III. Uncompromising Quality and Accuracy
The project must meet high standards for quality and correctness. The book MUST contain a minimum of 10 chapters and feature a fully responsive design. The RAG chatbot MUST achieve 95%+ accuracy on general content queries and 100% accuracy on pre-selected Q&A pairs. All TypeScript and Python code MUST be statically linted to enforce code quality and consistency.

### IV. Automated Development and Deployment
The project MUST be deployed to GitHub Pages via a fully automated GitHub Actions CI/CD pipeline, ensuring zero-downtime deployments. The end-to-end development workflow is strictly defined as: 1. Content generation with Spec-Kit, 2. Site build with Docusaurus, 3. RAG index creation, 4. Chatbot embedding, 5. Automated deployment.

### V. [PRINCIPLE_5_NAME]
TODO(Principles): Define principle for Observability, Versioning, or Simplicity.

### VI. [PRINCIPLE_6_NAME]
TODO(Principles): Define principle for Observability, Versioning, or Simplicity.

## Governance
This Constitution is the single source of truth for project principles and standards. All development, reviews, and architectural decisions must align with it. Amendments require a documented proposal, team consensus, and a clear migration plan for existing work. All pull requests must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-19 | **Last Amended**: 2025-12-19