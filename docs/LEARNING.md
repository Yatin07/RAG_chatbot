# 📚 Ultimate Learning Guide & Project Roadmap

Welcome! This guide is designed to take you from a complete beginner to an advanced developer by using this **RAG PDF Chatbot** codebase as your primary learning sandbox. 

It explains **every single file** in this project, its architectural role, and maps out a step-by-step syllabus from basic programming to advanced AI engineering and DevOps.

---

## 🗺️ Part 1: Step-by-Step Learning Syllabus (Basic to Advanced)

To understand this project fully, you should learn these topics in order:

### 🟢 Level 1: The Basics (Foundations)
1. **Python Programming:**
   - *Concepts:* Variables, functions, loops (`for` and `while`), conditional statements (`if-else`), error handling (`try-except`), and Object-Oriented Programming (OOP) classes.
   - *In this project:* Almost every file uses OOP. `src/main.py` handles CLI arguments and interactive loops.
2. **Virtual Environments & Package Management:**
   - *Concepts:* How python handles libraries, using `pip` to install packages, creating isolated virtual environments (`venv`), and writing config files like `pyproject.toml` and `requirements.txt`.
   - *In this project:* Isolated packages prevent conflicts with your computer's global packages.

### 🟡 Level 2: Version Control & DevOps Foundations
3. **Git & GitHub basics:**
   - *Concepts:* Commits, staging (`git add`), branches, cloning, pushing (`git push`), pulling, and ignoring temporary files via `.gitignore`.
4. **CI/CD Pipelines (Continuous Integration / Continuous Deployment):**
   - *Concepts:* Automating software testing. Understanding how GitHub Actions automatically builds, lints, and runs tests on your code on remote servers before deploying to PyPI.
   - *In this project:* Read `docs/CI_CD_EXPLAINED.md` for a full breakdown.
5. **Docker & Containerization:**
   - *Concepts:* Creating standard "containers" so your code runs identically on any machine in the world without manual environment setup.
   - *In this project:* The `Dockerfile` packages the chatbot so it can run inside a container.

### 🔴 Level 3: Advanced AI & RAG Engineering
6. **Large Language Models (LLMs) & Local AI:**
   - *Concepts:* What an LLM is, temperature settings, context windows, prompt engineering, and how **Ollama** runs AI models (`llama3.2:3b`) completely offline.
7. **Document Ingestion & Chunking:**
   - *Concepts:* Parsing text out of binary PDF files, and splitting text into overlaps (e.g., 1000 characters with 100 overlap) to keep semantic meaning without exceeding LLM memory limits.
8. **Vector Embeddings & Semantic Search:**
   - *Concepts:* How computers turn words into lists of numbers (vectors) representing their meaning, and how vector databases (like **FAISS**) use math (L2 distance/Cosine similarity) to search for text by meaning rather than exact keywords.
9. **LangChain Framework:**
   - *Concepts:* The industry-standard framework for chaining together retrievers, prompt templates, and local LLMs to form a fully operational RAG (Retrieval-Augmented Generation) pipeline.

---

## 📂 Part 2: Complete Codebase Directory & File Guide

Here is a map of every file in the repository and what it does:

### 1. Core Source Code (`src/`)
- **[`src/__init__.py`](file:///e:/RAG_chatbot/src/__init__.py)**
  - *What it is:* A special python file that marks the `src` folder as a package. 
  - *What it does:* It is kept clean to allow lazy imports, preventing import errors during test collection on CI.
- **[`src/config.py`](file:///e:/RAG_chatbot/src/config.py)**
  - *What it is:* Central configuration manager.
  - *What it does:* Reads settings from environment variables (your `.env` file) or falls back to secure default values. It sets things like LLM model names, vector store paths, chunk sizes, and retrieval parameters.
- **[`src/document_processor.py`](file:///e:/RAG_chatbot/src/document_processor.py)**
  - *What it is:* PDF Document Handler.
  - *What it does:* Scans your folder for PDF files, loads their raw text using `PyMuPDFLoader`, and splits the text into small overlapping segments (chunks) using `RecursiveCharacterTextSplitter`.
- **[`src/vector_store.py`](file:///e:/RAG_chatbot/src/vector_store.py)**
  - *What it is:* Semantic Memory Builder.
  - *What it does:* Takes your text chunks, converts them to numerical vectors using Ollama's `nomic-embed-text` model, and builds a **FAISS** index. It can save this index to disk or load it back.
- **[`src/rag_chain.py`](file:///e:/RAG_chatbot/src/rag_chain.py)**
  - *What it is:* The AI Brain (The RAG Pipeline).
  - *What it does:* Hooks the FAISS retriever up to your ChatOllama LLM using LangChain. When you ask a question, it finds the relevant PDF chunks, writes a prompt including those chunks as context, feeds it to the local LLM, and returns the response.
- **[`src/main.py`](file:///e:/RAG_chatbot/src/main.py)**
  - *What it is:* Main orchestrator and entry point.
  - *What it does:* Sets up the CLI args (e.g. `--rebuild`, `--interactive`), initializes the RAG components, and manages the interactive chat loop in the console.

### 2. Test Suite (`tests/`)
- **[`tests/test_config.py`](file:///e:/RAG_chatbot/tests/test_config.py)**
  - *What it is:* Config unit tests.
  - *What it does:* Asserts that defaults are set properly and that configuration can be overridden by environment variables.
- **[`tests/test_document_processor.py`](file:///e:/RAG_chatbot/tests/test_document_processor.py)**
  - *What it is:* Document processor tests.
  - *What it does:* Mocks PDF loaders and walk paths to test chunking, file discovery, and loading errors without needing real PDF files.
- **[`tests/test_integration.py`](file:///e:/RAG_chatbot/tests/test_integration.py)**
  - *What it is:* Full system tests.
  - *What it does:* Mocks out the document processor and vector database to verify that the chatbot initiates, loads index stores, and queries the RAG chain correctly end-to-end.

### 3. CI/CD & Project Configuration (Root)
- **[`Dockerfile`](file:///e:/RAG_chatbot/Dockerfile)** & **[`.dockerignore`](file:///e:/RAG_chatbot/.dockerignore)**
  - *What they do:* Build instructions to containerize the app. `.dockerignore` makes sure heavy local data or passwords aren't baked into the image.
- **[`.github/workflows/ci.yml`](file:///e:/RAG_chatbot/.github/workflows/ci.yml)**
  - *What it is:* The automation blueprint.
  - *What it does:* Commands GitHub runners to automatically test formatting (Black), linting (Ruff), import order (isort), run tests with coverage (PyTest), scan for leaked credentials (GitGuardian), and publish updates to PyPI.
- **[`.pre-commit-config.yaml`](file:///e:/RAG_chatbot/.pre-commit-config.yaml)**
  - *What it does:* Runs formatting checks locally on your computer every time you type `git commit` to prevent pushing broken formatting.
- **[`pyproject.toml`](file:///e:/RAG_chatbot/pyproject.toml)**
  - *What it is:* Modern Python packaging manifest.
  - *What it does:* Declares metadata (name, description, version, authors), specifies dependencies (like LangChain, FAISS, PyMuPDF), and configures tools like Black, Ruff, Mypy, and Pytest coverage rules.
- **[`.gitignore`](file:///e:/RAG_chatbot/.gitignore)**
  - *What it does:* Tells Git to ignore build folders, virtual environments (`venv`), local configuration keys (`.env`), and compiled vector database index files (`health_supplements/`).

---

## 🛠️ Part 3: Suggested Practice Exercises to Learn by Doing

1. **Alter the Chunk Size:** Open `src/config.py` and change `CHUNK_SIZE` from `1000` to `500`. Rebuild the database (`--rebuild`). Notice if the answers become more specific or if they lose context.
2. **Change the LLM temperature:** Try changing `temperature` from `0.7` to `0.1` (very analytical/robotic) or `1.0` (more creative/verbose) in `src/config.py` and see how LLM answers shift.
3. **Write a new test:** Open `tests/test_config.py` and write a test case to check if custom LLM max token thresholds are respected.
