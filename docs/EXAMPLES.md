# Usage Examples

## 📚 Table of Contents

- [Quick Start Examples](#-quick-start-examples)
- [Basic Usage](#-basic-usage)
- [Advanced Configuration](#-advanced-configuration)
- [Custom Integration](#-custom-integration)
- [Performance Optimization](#-performance-optimization)
- [Troubleshooting Examples](#-troubleshooting-examples)

## 🚀 Quick Start Examples

### 1. Basic Question Answering

```bash
# Install and setup
pip install -e .
ollama pull nomic-embed-text
ollama pull llama3.2:3b

# Ask a simple question
python -m src.main --question "What are the benefits of BCAA supplements?"

# Interactive mode
python -m src.main --interactive
```

### 2. Rebuild Vector Store

```bash
# Force rebuild of vector store from documents
python -m src.main --rebuild --question "What is muscle protein synthesis?"
```

### 3. Custom Configuration

```bash
# Use different LLM model
OLLAMA_BASE_URL=http://localhost:11434 LLM_MODEL=llama3.2:1b python -m src.main --question "Explain creatine supplementation"

# Smaller chunks for better precision
CHUNK_SIZE=500 CHUNK_OVERLAP=50 python -m src.main --question "What are the side effects of protein supplements?"
```

## 💡 Basic Usage

### Command Line Interface

```bash
# Help
python -m src.main --help

# Single question
python -m src.main --question "How does creatine work?"

# Interactive session
python -m src.main --interactive

# Rebuild and ask
python -m src.main --rebuild --question "What are BCAAs?"
```

### Programmatic Usage

```python
from src import RAGPDFChatbot

# Initialize chatbot
chatbot = RAGPDFChatbot()
chatbot.initialize()

# Ask questions
questions = [
    "What are the benefits of whey protein?",
    "How much protein should I consume daily?",
    "What are the side effects of creatine?"
]

for question in questions:
    answer = chatbot.ask(question)
    print(f"Q: {question}")
    print(f"A: {answer}")
    print("-" * 50)
```

### Batch Processing

```python
from src import RAGPDFChatbot

# Load questions from file
with open('questions.txt', 'r') as f:
    questions = [line.strip() for line in f if line.strip()]

# Process batch
chatbot = RAGPDFChatbot()
chatbot.initialize()

results = []
for i, question in enumerate(questions, 1):
    print(f"Processing question {i}/{len(questions)}")
    answer = chatbot.ask(question)
    results.append({
        'question': question,
        'answer': answer,
        'timestamp': datetime.now().isoformat()
    })

# Save results
import json
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## 🔧 Advanced Configuration

### Environment Variables

```bash
# Complete configuration
export OLLAMA_BASE_URL=http://localhost:11434
export EMBEDDING_MODEL=nomic-embed-text
export LLM_MODEL=llama3.2:3b
export LLM_TEMPERATURE=0.7
export LLM_MAX_TOKENS=512
export DATASET_PATH=./rag-dataset
export CHUNK_SIZE=1000
export CHUNK_OVERLAP=100
export VECTOR_STORE_PATH=./health_supplemets
export SAVE_VECTOR_STORE=true
export RETRIEVAL_TYPE=mmr
export RETRIEVAL_K=3
export RETRIEVAL_FETCH_K=100
export RETRIEVAL_LAMBDA=1.0
export LOG_LEVEL=INFO
```

### Custom Configuration File

```python
import os
from src.config import AppConfig, EmbeddingConfig, LLMConfig, DocumentProcessingConfig

# Create custom configuration
custom_config = AppConfig(
    embedding=EmbeddingConfig(
        model_name="nomic-embed-text",
        base_url="http://localhost:11434"
    ),
    llm=LLMConfig(
        model_name="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0.5,
        max_tokens=256
    ),
    document_processing=DocumentProcessingConfig(
        chunk_size=500,
        chunk_overlap=50,
        dataset_path="./custom-dataset"
    )
)

# Use with components
from src.document_processor import DocumentProcessor
processor = DocumentProcessor()
processor.dataset_path = custom_config.document_processing.dataset_path
processor.chunk_size = custom_config.document_processing.chunk_size
processor.chunk_overlap = custom_config.document_processing.chunk_overlap
```

### Multiple Vector Stores

```python
from src.vector_store import VectorStoreManager
from src.document_processor import DocumentProcessor

# Create separate managers for different domains
supplements_manager = VectorStoreManager()
fitness_manager = VectorStoreManager()

# Configure different paths
supplements_manager.vector_store_path = "./vector-stores/supplements"
fitness_manager.vector_store_path = "./vector-stores/fitness"

# Process different datasets
supplements_processor = DocumentProcessor()
supplements_processor.dataset_path = "./datasets/supplements"

fitness_processor = DocumentProcessor()
fitness_processor.dataset_path = "./datasets/fitness"

# Build vector stores
supplements_docs = supplements_processor.process_documents()
supplements_manager.create_vector_store(supplements_docs)

fitness_docs = fitness_processor.process_documents()
fitness_manager.create_vector_store(fitness_docs)
```

## 🔗 Custom Integration

### Web API with FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src import RAGPDFChatbot

app = FastAPI(title="RAG PDF Chatbot API")

# Initialize chatbot
chatbot = None

@app.on_event("startup")
async def startup_event():
    global chatbot
    chatbot = RAGPDFChatbot()
    chatbot.initialize()

class Question(BaseModel):
    question: str
    rebuild_vector_store: bool = False

class Answer(BaseModel):
    question: str
    answer: str
    timestamp: str

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    try:
        if question.rebuild_vector_store:
            chatbot.initialize(rebuild_vector_store=True)

        answer = chatbot.ask(question.question)
        return Answer(
            question=question.question,
            answer=answer,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Discord Bot Integration

```python
import discord
from discord.ext import commands
from src import RAGPDFChatbot

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
chatbot = None

@bot.event
async def on_ready():
    global chatbot
    print(f'Bot connected as {bot.user}')
    chatbot = RAGPDFChatbot()
    chatbot.initialize()

@bot.command(name='ask')
async def ask(ctx, *, question: str):
    """Ask a question about the PDF documents"""
    try:
        # Send typing indicator
        async with ctx.typing():
            answer = chatbot.ask(question)

        # Split long answers into chunks
        if len(answer) > 2000:
            chunks = [answer[i:i+2000] for i in range(0, len(answer), 2000)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(answer)

    except Exception as e:
        await ctx.send(f"Sorry, I encountered an error: {str(e)}")

@bot.command(name='rebuild')
async def rebuild(ctx):
    """Rebuild the vector store"""
    try:
        async with ctx.typing():
            chatbot.initialize(rebuild_vector_store=True)
        await ctx.send("Vector store rebuilt successfully!")
    except Exception as e:
        await ctx.send(f"Error rebuilding vector store: {str(e)}")

# Run bot
if __name__ == "__main__":
    bot.run('YOUR_BOT_TOKEN')
```

### Streamlit Web Interface

```python
import streamlit as st
from src import RAGPDFChatbot

# Page configuration
st.set_page_config(
    page_title="RAG PDF Chatbot",
    page_icon="📚",
    layout="wide"
)

# Initialize chatbot in session state
if 'chatbot' not in st.session_state:
    with st.spinner('Initializing chatbot...'):
        st.session_state.chatbot = RAGPDFChatbot()
        st.session_state.chatbot.initialize()

chatbot = st.session_state.chatbot

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")

    if st.button("🔄 Rebuild Vector Store"):
        with st.spinner('Rebuilding vector store...'):
            chatbot.initialize(rebuild_vector_store=True)
        st.success("Vector store rebuilt!")

    st.markdown("---")
    st.markdown("### 📊 Statistics")
    # Add statistics if available

# Main interface
st.title("📚 RAG PDF Chatbot")
st.markdown("Ask questions about your PDF documents!")

# Chat interface
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner('Thinking...'):
            response = chatbot.ask(prompt)
        st.markdown(response)

    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
```

## ⚡ Performance Optimization

### Memory Optimization

```python
# Reduce chunk size for lower memory usage
CHUNK_SIZE=500 CHUNK_OVERLAP=50 python -m src.main --question "test"

# Use smaller retrieval parameters
RETRIEVAL_K=2 RETRIEVAL_FETCH_K=50 python -m src.main --interactive

# Limit concurrent processing
MAX_WORKERS=2 python -c "
import concurrent.futures
from src import RAGPDFChatbot

def process_question(question):
    chatbot = RAGPDFChatbot()
    chatbot.initialize()
    return chatbot.ask(question)

questions = ['Q1', 'Q2', 'Q3']
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(process_question, questions))
"
```

### Caching Strategies

```python
import pickle
from functools import lru_cache
from src import RAGPDFChatbot

@lru_cache(maxsize=1000)
def cached_ask(question: str) -> str:
    """Cache answers for repeated questions"""
    if not hasattr(cached_ask, 'chatbot'):
        cached_ask.chatbot = RAGPDFChatbot()
        cached_ask.chatbot.initialize()

    return cached_ask.chatbot.ask(question)

# Use cached version
answer1 = cached_ask("What is creatine?")
answer2 = cached_ask("What is creatine?")  # Will use cache
```

### Batch Processing

```python
from src import RAGPDFChatbot
import asyncio

async def batch_process_questions(questions, batch_size=5):
    """Process questions in batches to manage memory"""
    chatbot = RAGPDFChatbot()
    chatbot.initialize()

    results = []
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(questions) + batch_size - 1)//batch_size}")

        batch_results = []
        for question in batch:
            answer = chatbot.ask(question)
            batch_results.append((question, answer))

        results.extend(batch_results)

        # Optional: Clear some memory between batches
        import gc
        gc.collect()

    return results

# Usage
questions = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]
results = asyncio.run(batch_process_questions(questions, batch_size=3))
```

## 🔧 Troubleshooting Examples

### Debug Configuration

```python
import logging
import os

# Enable debug logging
os.environ['LOG_LEVEL'] = 'DEBUG'
logging.basicConfig(level=logging.DEBUG)

from src import RAGPDFChatbot

# Create chatbot with debug info
chatbot = RAGPDFChatbot()
print("Chatbot created")

try:
    chatbot.initialize()
    print("Initialization successful")
except Exception as e:
    print(f"Initialization failed: {e}")
    import traceback
    traceback.print_exc()
```

### Test Components Individually

```python
# Test document processing
from src.document_processor import DocumentProcessor

processor = DocumentProcessor()
print(f"Dataset path: {processor.dataset_path}")
print(f"Chunk size: {processor.chunk_size}")

try:
    pdf_files = processor.discover_pdf_files()
    print(f"Found {len(pdf_files)} PDF files: {pdf_files}")

    documents = processor.load_documents()
    print(f"Loaded {len(documents)} documents")

    chunks = processor.chunk_documents(documents[:1])  # Test with first doc
    print(f"Created {len(chunks)} chunks")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

### Vector Store Debugging

```python
from src.vector_store import VectorStoreManager

manager = VectorStoreManager()
print("Vector store manager created")

try:
    # Test embedding model
    test_embedding = manager.embedding_model.embed_query("test")
    print(f"Embedding dimension: {len(test_embedding)}")

    # Test vector store creation
    from src.document_processor import DocumentProcessor
    processor = DocumentProcessor()
    documents = processor.process_documents()

    if documents:
        vector_store = manager.create_vector_store(documents[:1])  # Test with one doc
        print("Vector store created successfully")

        retriever = manager.get_retriever()
        print("Retriever created successfully")

        # Test retrieval
        docs = retriever.invoke("test query")
        print(f"Retrieved {len(docs)} documents")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

### Network and Ollama Debugging

```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Test embedding model
curl http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "nomic-embed-text", "prompt": "test"}'

# Test LLM model
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2:3b", "prompt": "Hello", "stream": false}'
```

### Configuration Validation

```python
from src.config import load_config
import os

# Test configuration loading
try:
    config = load_config()
    print("Configuration loaded successfully")
    print(f"LLM Model: {config.llm.model_name}")
    print(f"Dataset Path: {config.document_processing.dataset_path}")
    print(f"Vector Store Path: {config.vector_store.local_path}")

    # Validate paths
    import os.path
    if not os.path.exists(config.document_processing.dataset_path):
        print(f"Warning: Dataset path does not exist: {config.document_processing.dataset_path}")
    else:
        pdf_count = len([f for f in os.listdir(config.document_processing.dataset_path) if f.endswith('.pdf')])
        print(f"Found {pdf_count} PDF files in dataset")

except Exception as e:
    print(f"Configuration error: {e}")
    import traceback
    traceback.print_exc()
```

### Performance Profiling

```python
import cProfile
import pstats
from src import RAGPDFChatbot

# Profile initialization
print("Profiling initialization...")
pr = cProfile.Profile()
pr.enable()

chatbot = RAGPDFChatbot()
chatbot.initialize()

pr.disable()
stats = pstats.Stats(pr)
stats.sort_stats('cumulative').print_stats(20)

# Profile question answering
print("\nProfiling question answering...")
pr = cProfile.Profile()
pr.enable()

answer = chatbot.ask("What are the benefits of protein supplements?")

pr.disable()
stats = pstats.Stats(pr)
stats.sort_stats('cumulative').print_stats(20)

print(f"Answer: {answer[:200]}...")
```

## 🎯 Advanced Examples

### Custom Document Processing

```python
from src.document_processor import DocumentProcessor
from langchain_text_splitters import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF

class CustomDocumentProcessor(DocumentProcessor):
    """Custom processor with advanced text extraction"""

    def load_documents(self):
        """Enhanced document loading with metadata extraction"""
        pdf_files = self.discover_pdf_files()
        documents = []

        for pdf_file in pdf_files:
            try:
                # Use PyMuPDF directly for better control
                doc = fitz.open(pdf_file)

                for page_num in range(len(doc)):
                    page = doc[page_num]

                    # Extract text with layout preservation
                    text = page.get_text("text")

                    # Extract metadata
                    metadata = {
                        "source": pdf_file,
                        "page": page_num + 1,
                        "total_pages": len(doc),
                        "file_size": os.path.getsize(pdf_file),
                        "creation_date": doc.metadata.get("creationDate", ""),
                        "mod_date": doc.metadata.get("modDate", ""),
                    }

                    documents.append({
                        "page_content": text,
                        "metadata": metadata
                    })

                doc.close()

            except Exception as e:
                print(f"Failed to load {pdf_file}: {str(e)}")
                continue

        if not documents:
            raise RuntimeError("No documents were successfully loaded")

        return documents

    def chunk_documents(self, documents):
        """Custom chunking with overlap preservation"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],  # Preserve structure
            keep_separator=True
        )

        chunks = []
        for doc in documents:
            doc_chunks = text_splitter.split_text(doc["page_content"])

            for i, chunk in enumerate(doc_chunks):
                chunk_metadata = doc["metadata"].copy()
                chunk_metadata.update({
                    "chunk_id": i,
                    "total_chunks": len(doc_chunks),
                    "chunk_start": i * (self.chunk_size - self.chunk_overlap),
                    "chunk_end": (i + 1) * (self.chunk_size - self.chunk_overlap) + self.chunk_overlap
                })

                chunks.append({
                    "page_content": chunk,
                    "metadata": chunk_metadata
                })

        return chunks
```

### Custom Vector Store with Persistence

```python
from src.vector_store import VectorStoreManager
import json
import os
from datetime import datetime

class PersistentVectorStoreManager(VectorStoreManager):
    """Enhanced vector store with metadata persistence"""

    def save_vector_store(self, path=None):
        """Save vector store with metadata"""
        super().save_vector_store(path)

        save_path = path or self.vector_store_path
        metadata_path = f"{save_path}_metadata.json"

        metadata = {
            "created_at": datetime.now().isoformat(),
            "embedding_model": self.embedding_model.model,
            "embedding_dimension": len(self.embedding_model.embed_query("test")),
            "vector_count": self.vector_store.index.ntotal if self.vector_store else 0,
            "index_type": "FAISS",
            "metric": "L2",
            "configuration": {
                "chunk_size": getattr(self, 'chunk_size', 'unknown'),
                "chunk_overlap": getattr(self, 'chunk_overlap', 'unknown'),
            }
        }

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def load_vector_store(self, path=None):
        """Load vector store with metadata validation"""
        load_path = path or self.vector_store_path
        metadata_path = f"{load_path}_metadata.json"

        # Load metadata if exists
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            print(f"Loading vector store created at {metadata['created_at']}")
            print(f"Vector store contains {metadata['vector_count']} vectors")

        # Load the actual vector store
        super().load_vector_store(path)

    def get_statistics(self):
        """Get vector store statistics"""
        if not self.vector_store:
            return None

        return {
            "total_vectors": self.vector_store.index.ntotal,
            "dimension": self.vector_store.index.d,
            "is_trained": self.vector_store.index.is_trained,
            "metric_type": "L2",  # FAISS default
        }
```

---

**🎉 Explore, Experiment, and Build Amazing Things!**
