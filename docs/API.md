# API Reference

## 📚 Table of Contents

- [Core Classes](#-core-classes)
- [Configuration Classes](#-configuration-classes)
- [Main Interface](#-main-interface)
- [Exception Handling](#-exception-handling)
- [Examples](#-examples)

## 🔧 Core Classes

### RAGPDFChatbot

The main application class that orchestrates the entire RAG pipeline.

#### Constructor

```python
RAGPDFChatbot()
```

**Returns:** `RAGPDFChatbot` instance

**Description:** Initializes the chatbot with all required components.

#### Methods

##### `initialize(rebuild_vector_store: bool = False) -> None`

Initialize the application and prepare for question answering.

**Parameters:**
- `rebuild_vector_store` (bool, optional): Whether to rebuild vector store from scratch. Defaults to `False`.

**Raises:**
- `RuntimeError`: If document processing or vector store initialization fails

##### `ask(question: str) -> str`

Ask a question using the RAG pipeline.

**Parameters:**
- `question` (str): Question to answer

**Returns:** `str` - Answer to the question

**Raises:**
- `RuntimeError`: If application is not initialized

##### `interactive_mode() -> None`

Run the application in interactive mode allowing multiple questions in a session.

### DocumentProcessor

Handles loading and processing of PDF documents.

#### Constructor

```python
DocumentProcessor()
```

**Returns:** `DocumentProcessor` instance

#### Methods

##### `discover_pdf_files() -> List[str]`

Discover all PDF files in the dataset directory.

**Returns:** `List[str]` - List of file paths to PDF documents

**Raises:**
- `FileNotFoundError`: If no PDF files are found

##### `load_documents() -> List[Dict[str, Any]]`

Load all PDF documents from the dataset.

**Returns:** `List[Dict[str, Any]]` - List of document objects

**Raises:**
- `RuntimeError`: If no documents are successfully loaded

##### `chunk_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]`

Split documents into chunks for embedding.

**Parameters:**
- `documents` (List[Dict[str, Any]]): List of document objects

**Returns:** `List[Dict[str, Any]]` - List of document chunks

##### `process_documents() -> List[Dict[str, Any]]`

Complete document processing pipeline.

**Returns:** `List[Dict[str, Any]]` - List of processed document chunks

### VectorStoreManager

Manages document embedding and vector storage.

#### Constructor

```python
VectorStoreManager()
```

**Returns:** `VectorStoreManager` instance

#### Methods

##### `create_vector_store(documents: List[Dict[str, Any]]) -> FAISS`

Create and populate vector store with document embeddings.

**Parameters:**
- `documents` (List[Dict[str, Any]]): List of document chunks to embed

**Returns:** `FAISS` - Populated vector store

##### `get_retriever() -> Any`

Get a retriever configured with current settings.

**Returns:** `Any` - Configured retriever object

**Raises:**
- `RuntimeError`: If vector store is not initialized

##### `save_vector_store(path: Optional[str] = None) -> None`

Save vector store to local storage.

**Parameters:**
- `path` (str, optional): Path to save vector store

**Raises:**
- `RuntimeError`: If vector store is not initialized

##### `load_vector_store(path: Optional[str] = None) -> FAISS`

Load vector store from local storage.

**Parameters:**
- `path` (str, optional): Path to load vector store from

**Returns:** `FAISS` - Loaded vector store

##### `vector_store_exists(path: Optional[str] = None) -> bool`

Check if vector store exists at specified path.

**Parameters:**
- `path` (str, optional): Path to check

**Returns:** `bool` - True if vector store exists

### RAGChain

Implements the Retrieval-Augmented Generation pipeline.

#### Constructor

```python
RAGChain(retriever: Any)
```

**Parameters:**
- `retriever` (Any): Document retriever object

**Returns:** `RAGChain` instance

#### Methods

##### `ask_question(question: str) -> str`

Ask a question using the RAG pipeline.

**Parameters:**
- `question` (str): Question to answer

**Returns:** `str` - Answer to the question

**Raises:**
- `RuntimeError`: If RAG chain is not initialized

##### `get_chain() -> Any`

Get the RAG chain object.

**Returns:** `Any` - RAG chain object

## ⚙️ Configuration Classes

### AppConfig

Main application configuration dataclass.

#### Attributes

- `embedding: EmbeddingConfig` - Embedding model configuration
- `llm: LLMConfig` - LLM model configuration
- `vector_store: VectorStoreConfig` - Vector store configuration
- `retrieval: RetrievalConfig` - Retrieval configuration
- `document_processing: DocumentProcessingConfig` - Document processing configuration

### EmbeddingConfig

Configuration for embedding models.

#### Attributes

- `model_name: str` - Model name (default: "nomic-embed-text")
- `base_url: str` - Ollama base URL (default: "http://localhost:11434")
- `dimension: Optional[int]` - Embedding dimension (default: None)

### LLMConfig

Configuration for LLM models.

#### Attributes

- `model_name: str` - Model name (default: "llama3.2:3b")
- `base_url: str` - Ollama base URL (default: "http://localhost:11434")
- `temperature: float` - Generation temperature (default: 0.7)
- `max_tokens: int` - Maximum tokens (default: 512)

### VectorStoreConfig

Configuration for vector store.

#### Attributes

- `index_type: str` - Index type (default: "flat")
- `metric: str` - Distance metric (default: "L2")
- `save_local: bool` - Save locally (default: True)
- `local_path: str` - Local path (default: "health_supplemets")

### RetrievalConfig

Configuration for document retrieval.

#### Attributes

- `search_type: str` - Search type (default: "mmr")
- `k: int` - Number of documents (default: 3)
- `fetch_k: int` - Number to fetch (default: 100)
- `lambda_mult: float` - MMR lambda (default: 1.0)

### DocumentProcessingConfig

Configuration for document processing.

#### Attributes

- `chunk_size: int` - Chunk size (default: 1000)
- `chunk_overlap: int` - Chunk overlap (default: 100)
- `dataset_path: str` - Dataset path (default: "rag-dataset")

## 🎯 Main Interface

### CLI Interface

The application can be run via command line with the following options:

```bash
python -m src.main [OPTIONS]

Options:
  --rebuild           Rebuild vector store from scratch
  --interactive       Run in interactive mode
  --question TEXT     Ask a specific question
  --help              Show help message
```

### Programmatic Interface

```python
from src import RAGPDFChatbot

# Initialize chatbot
chatbot = RAGPDFChatbot()
chatbot.initialize()

# Ask questions
answer = chatbot.ask("What are the benefits of BCAA supplements?")
print(answer)

# Interactive mode
chatbot.interactive_mode()
```

## 🚨 Exception Handling

### RuntimeError
- Raised when application is not properly initialized
- Raised when vector store operations fail
- Raised when document processing fails

### FileNotFoundError
- Raised when no PDF files are found in dataset directory

### ValueError
- Raised for invalid configuration values
- Raised for invalid input parameters

## 📝 Examples

### Basic Usage

```python
from src import RAGPDFChatbot

# Create and initialize chatbot
chatbot = RAGPDFChatbot()
chatbot.initialize()

# Ask a question
question = "What are the benefits of BCAA supplements?"
answer = chatbot.ask(question)
print(f"Answer: {answer}")
```

### Configuration

```python
import os
from src.config import config

# Set environment variables before importing
os.environ["LLM_MODEL"] = "llama3.2:1b"
os.environ["CHUNK_SIZE"] = "500"

# Config will use the new values
print(f"Model: {config.llm.model_name}")
print(f"Chunk size: {config.document_processing.chunk_size}")
```

### Custom Configuration

```python
from src.config import EmbeddingConfig, LLMConfig, AppConfig

# Create custom config
custom_config = AppConfig(
    embedding=EmbeddingConfig(model_name="custom-embedding"),
    llm=LLMConfig(model_name="custom-llm", temperature=0.5),
    # ... other configs
)

# Use with components
processor = DocumentProcessor()
processor.dataset_path = custom_config.document_processing.dataset_path
```

### Error Handling

```python
from src import RAGPDFChatbot

chatbot = RAGPDFChatbot()

try:
    # This will fail if not initialized
    answer = chatbot.ask("Test question")
except RuntimeError as e:
    print(f"Error: {e}")
    # Initialize first
    chatbot.initialize()
    answer = chatbot.ask("Test question")
```

## 🔗 Related Documentation

- [README.md](../README.md) - Project overview and quick start
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture details
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](../SECURITY.md) - Security policy
