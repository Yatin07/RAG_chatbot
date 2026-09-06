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

---

## Module 2: The Memory - Embeddings & Vector Storage (FAISS)

### Step 2a: Text Embeddings (`OllamaEmbeddings`)
- **Concept:** Converting words into high-dimensional mathematical vectors so computers can understand "semantic meaning."

```python
# from src.vector_store.py
from langchain_ollama import OllamaEmbeddings

self.embedding_model = OllamaEmbeddings(
    model="nomic-embed-text", 
    base_url="http://localhost:11434"
)
test_embedding = self.embedding_model.embed_query("test")
```

- **Technical Syntax Breakdown:**
  - `OllamaEmbeddings`: *Why this class?* It connects LangChain to your local Ollama instance, ensuring your data never leaves your computer (crucial for privacy).
  - `model="nomic-embed-text"`: *Why this specific model?* It is an embedding model specifically trained to convert text into arrays of numbers (e.g., 768 floating-point numbers). It maps concepts like "dog" and "puppy" mathematically close together in vector space.
  - `embed_query("test")`: *Why do this in the code?* The system does a dummy test run to dynamically figure out the `embedding_dim` (the size of the vector array). FAISS needs to know this exact dimension before it can create an index.

### Step 2b: Building the FAISS Database
- **Concept:** Storing millions of vectors in a way that allows lightning-fast mathematical searches.

```python
# from src.vector_store.py
import faiss
from langchain_community.vectorstores import FAISS

# Initializing the index
embedding_dim = len(test_embedding)
index = faiss.IndexFlatL2(embedding_dim)

# Creating the LangChain wrapper
self.vector_store = FAISS(
    embedding_function=self.embedding_model,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)
```

- **Technical Syntax Breakdown:**
  - `faiss.IndexFlatL2(embedding_dim)`: *Why FAISS and why L2?* FAISS (Facebook AI Similarity Search) is an ultra-fast C++ library for vector search. `IndexFlatL2` tells FAISS to calculate the **Euclidean Distance** (L2 norm) between vectors to find the closest matches. It computes the direct, straight-line distance between the user's question vector and the document vectors.
  - `docstore=InMemoryDocstore()`: *Why?* FAISS itself *only* stores the math (vectors). The `InMemoryDocstore` is a LangChain helper that acts as a dictionary, mapping the mathematical vector ID back to the actual readable English text string so the LLM can read it later.

### Step 2c: The Retriever (`as_retriever`)
- **Concept:** Creating the actual search engine configuration.

```python
# from src.vector_store.py
return self.vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 100,
        "lambda_mult": 1.0,
    }
)
```

- **Technical Syntax Breakdown:**
  - `search_type="mmr"`: Maximal Marginal Relevance. *Why not just normal similarity?* Normal similarity might return 3 chunks that all say the exact same thing. MMR fixes this by fetching a large pool of similar chunks (`fetch_k=100`), and then carefully selecting the top `k=3` chunks that are mathematically similar to the query, but *dissimilar from each other*. This provides the LLM with a diverse set of facts instead of redundant noise.

---

## Module 3: The Brain - RAG & LangChain

### Step 3a: The Generator (`ChatOllama`)
- **Concept:** Setting up the actual "Brain" (Large Language Model) that will write the final answer.

```python
# from src.rag_chain.py
from langchain_ollama import ChatOllama

self.llm = ChatOllama(
    model="llama3.2:3b",
    base_url="http://localhost:11434",
    temperature=0.7,
)
```

- **Technical Syntax Breakdown:**
  - `ChatOllama`: *Why?* This class allows LangChain to communicate directly with the local Ollama server holding the Llama 3.2 model.
  - `model="llama3.2:3b"`: *Why this model?* The `3b` refers to 3 billion parameters. It is extremely lightweight, meaning it can run entirely on a standard laptop CPU without needing a massive GPU.
  - `temperature=0.7`: *Why 0.7?* Temperature controls the randomness/creativity of the model. `0.0` is strictly analytical and deterministic (good for pure facts). `1.0` is highly creative (good for poetry). `0.7` provides a balance—generating natural, fluent language without completely hallucinating facts.

### Step 3b: Prompt Engineering (`ChatPromptTemplate`)
- **Concept:** Injecting strict instructions and our FAISS context into the LLM's brain.

```python
# from src.rag_chain.py
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "Question:{question}\n\n"
    "Context:{context}\n\n"
    "Answer:"
)
self.prompt = ChatPromptTemplate.from_template(template)
```

- **Technical Syntax Breakdown:**
  - `ChatPromptTemplate.from_template()`: *Why?* This turns a standard Python string into a dynamic template. At runtime, LangChain will hunt for the `{question}` and `{context}` placeholders and dynamically inject the user's input and the FAISS database results directly into those slots.
  - *Why give it such strict instructions?* LLMs are naturally designed to just predict the next word. If you don't explicitly say "Use the following pieces of retrieved context," the LLM will ignore the FAISS database and just hallucinate an answer based on its pre-training data.

### Step 3c: The LCEL Pipeline (LangChain Expression Language)
- **Concept:** Piping the data through the system like water through a plumbing system.

```python
# from src.rag_chain.py
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

self.chain = (
    {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
    | self.prompt
    | self.llm
    | StrOutputParser()
)
```

- **Technical Syntax Breakdown:**
  - `|` (The Pipe Operator): *Why?* This is LCEL syntax. It passes the output of the left side directly as the input to the right side, drastically reducing boilerplate code.
  - `self.retriever | format_docs`: Takes the user's question, searches FAISS, and then joins the resulting chunks into a single readable text string.
  - `RunnablePassthrough()`: *Why?* It acts as a transparent mirror. It simply grabs the user's raw question (e.g., "What is BCAA?") and passes it directly into the `{question}` slot of the prompt.
  - `StrOutputParser()`: *Why?* The raw output from the `ChatOllama` model is a complex JSON/Object containing metadata, token usage, etc. This parser cleanly extracts just the final text string to show to the user.

---

## Module 4: The Orchestration (Tying It Together)

### Step 4a: Command Line Interface (CLI) with `argparse`
- **Concept:** Allowing the user to control the application from the terminal using flags like `--rebuild`.

```python
# from src.main.py
import argparse

parser = argparse.ArgumentParser(description="RAG PDF Chatbot")
parser.add_argument("--rebuild", action="store_true", help="Rebuild vector store")
parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
args = parser.parse_args()
```

- **Technical Syntax Breakdown:**
  - `argparse`: *Why?* It is the Python standard library for building command-line interfaces. It automatically generates help messages (`--help`) and parses the terminal arguments into a Python object (`args`).
  - `action="store_true"`: *Why?* This means the flag doesn't need a value. If the user types `--rebuild`, `args.rebuild` becomes `True`. If they don't type it, it defaults to `False`.

### Step 4b: Smart Initialization (Caching the FAISS Index)
- **Concept:** Avoiding the slow process of re-reading PDFs and re-embedding them every time you restart the app.

```python
# from src.main.py
def initialize(self, rebuild_vector_store: bool = False):
    if not rebuild_vector_store and self.vector_store_manager.vector_store_exists():
        print("Loading existing vector store...")
        self.vector_store_manager.load_vector_store()
    else:
        print("Building vector store from documents...")
        documents = self.document_processor.process_documents()
        self.vector_store_manager.create_vector_store(documents)
```

- **Technical Syntax Breakdown:**
  - `vector_store_exists()`: Checks the hard drive for the `health_supplements/` folder. 
  - *Why this if/else block?* Embedding a massive PDF can take minutes. If the FAISS index is already saved to the disk (and the user didn't explicitly pass `--rebuild`), we instantly load it from disk in seconds. We only trigger the heavy `document_processor` if the database doesn't exist yet.

### Step 4c: The Interactive Loop
- **Concept:** Creating a persistent chat session so the app doesn't close after one question.

```python
# from src.main.py
def interactive_mode(self):
    while True:
        question = input("Ask a question: ").strip()
        if question.lower() in ["quit", "exit", "q"]:
            break
        answer = self.ask(question)
        print(answer)
```

- **Technical Syntax Breakdown:**
  - `while True:`: *Why?* Creates an infinite loop, keeping the Python process alive so the user can ask follow-up questions.
  - `input()`: Blocks the loop and waits for the user to type in the terminal.
  - `break`: The only way to exit the infinite loop (triggered if the user types "quit").
