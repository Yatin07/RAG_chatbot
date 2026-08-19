# 📚 Learning Guide: RAG PDF Chatbot

Welcome! If you are completely new to AI, Python, or the concept of RAG (Retrieval-Augmented Generation), this guide is designed for you. It provides a **chronological roadmap** to learn all the technologies used in this project from scratch.

## 🗺️ The Learning Roadmap

To truly understand how this project works, it's best to learn the underlying technologies in a specific order:

1. **Python Fundamentals** (The Foundation)
2. **Virtual Environments & Package Management** (The Setup)
3. **Core AI Concepts & Local LLMs** (The Brains)
4. **LangChain & RAG** (The Framework)
5. **Vector Databases & FAISS** (The Memory)
6. **Understanding this Project's Codebase** (Putting it all together)

---

### Step 1: Python Fundamentals 🐍
This project is built entirely in Python. You don't need to be an expert, but you need to understand the basics to read the code.

- **What to learn**: Variables, Data Structures (Lists, Dictionaries), Functions, Classes (Object-Oriented Programming), and File I/O.
- **Why we use it**: It is the industry standard language for AI and Data Science.
- **Resources**: 
  - [Python for Beginners (FreeCodeCamp)](https://www.youtube.com/watch?v=rfscVS0vtbw)
  - [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)

### Step 2: Environment Management & Tooling ⚙️
Before running AI models, you must know how to manage dependencies so your code doesn't break other projects on your computer.

- **What to learn**: `pip`, `venv` (Virtual Environments), and `.env` files (Environment Variables).
- **Why we use it**: To keep project dependencies (like LangChain or FAISS) isolated. The `.env` file securely stores configurations without hardcoding them into the app.
- **Resources**: 
  - [Python Virtual Environments Explained](https://realpython.com/python-virtual-environments-a-primer/)

### Step 3: Local Large Language Models (LLMs) with Ollama 🦙
Instead of paying for OpenAI's API (like ChatGPT), this project runs AI models directly on your computer.

- **What to learn**: What an LLM is, how prompting works, and how to use Ollama.
- **Why we use it**: **Ollama** allows us to run models like `llama3.2:3b` and `nomic-embed-text` locally, ensuring 100% privacy for your PDF data.
- **Resources**: 
  - [Ollama Official Website](https://ollama.com/) (Install it and try running `ollama run llama3.2` in your terminal!)

### Step 4: The Core Concept: What is RAG? 🧠
RAG stands for **Retrieval-Augmented Generation**. LLMs only know what they were trained on. If you ask an LLM about your personal PDF, it won't know the answer and might hallucinate (make things up). RAG solves this by:
1. **Retrieving** relevant text from your PDF.
2. **Augmenting** your question with that text.
3. **Generating** an answer based *only* on the text we just gave it.

- **Resources**: 
  - [IBM: What is RAG?](https://research.ibm.com/blog/retrieval-augmented-generation-RAG)

### Step 5: LangChain & Document Processing 🦜🔗
LangChain is a powerful framework that makes building RAG applications much easier.

- **What to learn**: Document Loaders, Text Splitters, and Chains.
- **Why we use it**: 
  - **PyMuPDF / LangChain Loaders**: To extract the raw text out of PDF files.
  - **Text Splitters**: A 100-page PDF is too big to send to an LLM all at once. LangChain splits it into small "chunks" (e.g., 1000 characters each).
- **Resources**: 
  - [LangChain Crash Course](https://www.youtube.com/watch?v=aywZrzNaKjs)

### Step 6: Embeddings and Vector Databases (FAISS) 🗄️
How does the system find the *right* PDF chunk to answer your question out of thousands of chunks? Math!

- **What to learn**: Vector Embeddings and FAISS (Facebook AI Similarity Search).
- **Why we use it**: 
  - **Embeddings**: Converts text chunks into long lists of numbers (vectors). Sentences with similar meanings have similar numbers.
  - **FAISS**: A highly optimized database that stores these vectors and instantly finds the chunks that are mathematically most similar to your question.
- **Resources**: 
  - [Illustrated Guide to Vector Databases](https://www.pinecone.io/learn/vector-database/)

---

## 🏗️ How to Read This Project's Code

Now that you know the theory, here is how you should read the files in this repository chronologically to understand the flow:

1. **`src/config.py`**: Start here. See how the application loads settings from the `.env` file.
2. **`src/document_processor.py`**: Look at how PDFs are loaded and split into chunks.
3. **`src/vector_store.py`**: See how those chunks are converted to vectors and saved into FAISS.
4. **`src/rag_chain.py`**: The magic happens here. See how LangChain takes a user's question, finds the vectors, and asks the Ollama LLM.
5. **`src/main.py`**: The entry point. See how all the above components are tied together into a running application.

## 📝 Practice Exercise for Beginners
1. Install Ollama and pull the models (`llama3.2:3b` and `nomic-embed-text`).
2. Run `python -m src.main --rebuild --interactive` to build the database from your PDFs and start chatting.
3. Open `src/config.py` and try changing the `CHUNK_SIZE` from `1000` to `500`. Rebuild the database. Notice if the answers become more specific or if they lose context!

---
*Happy Learning! Feel free to refer back to this document whenever you get stuck on a specific technology.*
