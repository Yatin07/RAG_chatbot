# RAG PDF Chatbot - Course Lessons & Deep Dives

This document contains the detailed explanations, analogies, and code breakdowns from our teaching sessions. It serves as your primary textbook for understanding the codebase.

---

## Module 1: Document Processing (The Foundation)

### Step 1a: Extracting Text from PDFs (`PyMuPDFLoader`)
- **Concept:** Reading binary PDF files and extracting raw text for the LLM.

```python
# from src.document_processor.py
from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader(file_path)
documents = loader.load()
```

- **Technical Syntax Breakdown:**
  - `PyMuPDFLoader(file_path)`: Instantiates the document loader. *Why PyMuPDF?* It's an industry standard that is significantly faster and more accurate at parsing complex PDF layouts (like columns, embedded fonts, or tables) compared to older libraries like PyPDF2.
  - `loader.load()`: *Why?* This executes the underlying C++ backend of PyMuPDF to parse the binary file, returning a list of LangChain `Document` objects. Each object contains the raw text (`page_content`) and metadata (like the page number, which is crucial if you want the chatbot to cite its sources).

### Step 1b: The Context Window & Chunking (`RecursiveCharacterTextSplitter`)
- **Concept:** Breaking large text into overlapping blocks so it fits into the LLM's memory limits and ensures accurate vector searches.

```python
# from src.document_processor.py
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
chunks = text_splitter.split_documents(documents)
```

- **Technical Syntax Breakdown:**
  - `RecursiveCharacterTextSplitter`: *Why this specific splitter?* It is the absolute standard for RAG. It splits text hierarchically: first it tries to split by double newlines (`\n\n` - paragraphs), then single newlines (`\n` - lines), then spaces (words). This guarantees it will preserve semantic meaning by not breaking a sentence in half unless the sentence itself is larger than 1000 characters.
  - `chunk_size=1000`: The maximum number of characters per chunk. *Why?* To respect the LLM's "Context Window" limit. Additionally, smaller chunks make vector searches highly precise (searching 1000 characters yields much better semantic matches than trying to match a query against a massive 10,000-character wall of text).
  - `chunk_overlap=100`: Replicates 100 characters from the end of Chunk 1 to the beginning of Chunk 2. *Why?* If a crucial thought spans across the 1000-character boundary, it would be torn in two. Overlap ensures that the context around the boundary is preserved in both chunks.
  - `split_documents(documents)`: *Why?* This executes the splitting logic over the previously loaded PDF pages and returns an array of hundreds of smaller `Document` objects, ready to be converted into math in the next step.
