# RAG PDF Chatbot - Teaching Plan

This plan is designed to take you from understanding the basic concepts to mastering the codebase for your interview. We will tackle this module by module.

## Module 1: The Foundation - Document Processing
**Goal:** Understand how we extract text from PDFs and prepare it for the AI.
*   **Concepts:** PDF Parsing, Text Chunking, Overlap, LLM Context Windows.
*   **Core Files:** `src/document_processor.py`, `src/config.py` (Chunk size settings).
*   **Outcome:** You will be able to explain *why* and *how* we break down large documents.

## Module 2: The Memory - Embeddings & Vector Storage
**Goal:** Understand how the AI "memorizes" and searches text.
*   **Concepts:** Vector Embeddings (`nomic-embed-text`), FAISS Vector Database, Semantic Search (Cosine Similarity).
*   **Core Files:** `src/vector_store.py`.
*   **Outcome:** You will be able to explain how text is converted to math so the computer can find relevant information instantly.

## Module 3: The Brain - RAG & LangChain
**Goal:** Understand how we connect the database to the actual AI model to generate answers.
*   **Concepts:** LangChain Framework, Prompt Engineering, Local LLMs (`llama3.2`), Retrieval-Augmented Generation (RAG).
*   **Core Files:** `src/rag_chain.py`.
*   **Outcome:** You will be able to explain the core RAG loop: User asks question -> Search FAISS -> Inject into Prompt -> LLM answers.

## Module 4: The Orchestration
**Goal:** See how everything is tied together into a working application.
*   **Concepts:** Application flow, Environment Variables, CLI interfaces.
*   **Core Files:** `src/main.py`, `.env`.
*   **Outcome:** You will understand how data flows from the user's terminal, through the entire system, and back.

---
**How we will proceed:**
We will start with **Module 1**. I will explain the concepts and the code. Then, I will document the notes in `COURSE_LESSONS.md` and generate the relevant interview questions in `INTERVIEW_QA.md`. When you are ready to move on, just tell me!
