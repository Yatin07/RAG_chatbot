"""
Vector store module for RAG PDF Chatbot.

This module handles document embedding, vector storage, and retrieval
using FAISS and Ollama embeddings.
"""

import os
import warnings
import faiss
from typing import List, Dict, Any, Optional
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from src.config import config

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

class VectorStoreManager:
    """
    Manages document embedding and vector storage.

    Responsibilities:
    - Create embeddings using Ollama
    - Store and retrieve vectors using FAISS
    - Handle vector store persistence
    """

    def __init__(self):
        """Initialize vector store manager with configuration."""
        self.embedding_model = self._initialize_embedding_model()
        self.vector_store = None
        self.index = None

    def _initialize_embedding_model(self) -> OllamaEmbeddings:
        """
        Initialize the embedding model.

        Returns:
            OllamaEmbeddings: Configured embedding model
        """
        return OllamaEmbeddings(
            model=config.embedding.model_name,
            base_url=config.embedding.base_url
        )

    def _initialize_vector_store(self) -> FAISS:
        """
        Initialize FAISS vector store with appropriate index.

        Returns:
            FAISS: Configured vector store
        """
        # Get embedding dimension by embedding a test string
        test_embedding = self.embedding_model.embed_query("test")
        embedding_dim = len(test_embedding)

        # Create FAISS index
        if config.vector_store.metric == "L2":
            index = faiss.IndexFlatL2(embedding_dim)
        else:
            index = faiss.IndexFlatIP(embedding_dim)

        return FAISS(
            embedding_function=self.embedding_model,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )

    def create_vector_store(self, documents: List[Dict[str, Any]]) -> FAISS:
        """
        Create and populate vector store with document embeddings.

        Args:
            documents: List of document chunks to embed

        Returns:
            FAISS: Populated vector store
        """
        self.vector_store = self._initialize_vector_store()
        self.vector_store.add_documents(documents)
        return self.vector_store

    def get_retriever(self) -> Any:
        """
        Get a retriever configured with current settings.

        Returns:
            Any: Configured retriever object
        """
        if not self.vector_store:
            raise RuntimeError("Vector store not initialized")

        return self.vector_store.as_retriever(
            search_type=config.retrieval.search_type,
            search_kwargs={
                'k': config.retrieval.k,
                'fetch_k': config.retrieval.fetch_k,
                'lambda_mult': config.retrieval.lambda_mult
            }
        )

    def save_vector_store(self, path: Optional[str] = None) -> None:
        """
        Save vector store to local storage.

        Args:
            path: Optional path to save vector store
        """
        if not self.vector_store:
            raise RuntimeError("Vector store not initialized")

        save_path = path or config.vector_store.local_path
        self.vector_store.save_local(save_path)

    def load_vector_store(self, path: Optional[str] = None) -> FAISS:
        """
        Load vector store from local storage.

        Args:
            path: Optional path to load vector store from

        Returns:
            FAISS: Loaded vector store
        """
        load_path = path or config.vector_store.local_path
        self.vector_store = FAISS.load_local(
            load_path,
            embeddings=self.embedding_model,
            allow_dangerous_deserialization=True
        )
        return self.vector_store

    def vector_store_exists(self, path: Optional[str] = None) -> bool:
        """
        Check if vector store exists at specified path.

        Args:
            path: Optional path to check

        Returns:
            bool: True if vector store exists
        """
        check_path = path or config.vector_store.local_path
        return os.path.exists(check_path) and os.path.isdir(check_path)
