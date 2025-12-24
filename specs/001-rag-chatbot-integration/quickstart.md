# Quickstart: Frontend-Backend Integration for RAG Chatbot

This guide provides instructions to quickly set up and run the Docusaurus frontend and FastAPI RAG agent backend, allowing you to test their integration.

## 1. Overview

You will set up the local development environment for both the RAG agent backend and the Docusaurus frontend, then verify that user queries from the Docusaurus site are processed by the RAG agent and responses are displayed.

## 2. Prerequisites

Before you begin, ensure you have the following installed:
-   **Git**: For cloning the repository.
-   **Python 3.8+**: For the FastAPI backend.
-   **Node.js 18+ and npm**: For the Docusaurus frontend.

## 3. Backend Setup (FastAPI RAG Agent)

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```
2.  **Create and activate a Python virtual environment**:
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source ./.venv/bin/activate
    ```
3.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Start the FastAPI application**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend should now be running, typically on `http://127.0.0.1:8000`. Keep this terminal open.

## 4. Frontend Setup (Docusaurus Book)

1.  **Open a new terminal and navigate to the Docusaurus directory**:
    ```bash
    cd ros2-docs
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install
    ```
3.  **Start the Docusaurus development server**:
    ```bash
    npm run start
    ```
    The Docusaurus site should open in your browser, typically at `http://localhost:3000`. Keep this terminal open.

## 5. Testing the Integration

1.  **Access the Docusaurus site**: Ensure the Docusaurus development server is running and accessible in your web browser (usually `http://localhost:3000`).
2.  **Locate the Chatbot UI**: Find the integrated RAG chatbot component on the Docusaurus site (e.g., a floating button, a sidebar component, or integrated into a specific page as per the final UI implementation).
3.  **Submit a Query**:
    *   Type a question into the chatbot's input field (e.g., "What is ROS 2?").
    *   Submit the query.
4.  **Verify Response**: Observe that the chatbot displays a response from the RAG agent. You should also see activity in both the backend and frontend terminal windows as the request and response are processed.
5.  **Test with Selected Text (if implemented in UI)**:
    *   Select a piece of text on any Docusaurus page.
    *   Use the UI mechanism (e.g., a context menu option, a specific button) to submit a query based on this selected text.
    *   Verify that the RAG agent's response considers the selected text as context.

This completes the quickstart guide. You now have the full frontend-backend RAG chatbot integration running locally.
