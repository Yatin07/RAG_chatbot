"""
Configuration module for RAG PDF Chatbot.

This module handles all configuration settings, environment variables,
and application constants in a centralized manner.
"""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class EmbeddingConfig:
    """Configuration for embedding models."""

    model_name: str = "nomic-embed-text"
    base_url: str = "http://localhost:11434"
    dimension: Optional[int] = None


@dataclass
class LLMConfig:
    """Configuration for LLM models."""

    model_name: str = "llama3.2:3b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7
    max_tokens: int = 512


@dataclass
class VectorStoreConfig:
    """Configuration for vector store."""

    index_type: str = "flat"
    metric: str = "L2"
    save_local: bool = True
    local_path: str = "health_supplements"


@dataclass
class RetrievalConfig:
    """Configuration for document retrieval."""

    search_type: str = "mmr"
    k: int = 3
    fetch_k: int = 100
    lambda_mult: float = 1.0


@dataclass
class DocumentProcessingConfig:
    """Configuration for document processing."""

    chunk_size: int = 1000
    chunk_overlap: int = 100
    dataset_path: str = "rag-dataset"


@dataclass
class AppConfig:
    """Main application configuration."""

    embedding: EmbeddingConfig
    llm: LLMConfig
    vector_store: VectorStoreConfig
    retrieval: RetrievalConfig
    document_processing: DocumentProcessingConfig


def load_config() -> AppConfig:
    """
    Load application configuration from environment variables and defaults.

    Returns:
        AppConfig: Application configuration object
    """
    # Load from environment variables if available, otherwise use defaults
    embedding_config = EmbeddingConfig(
        model_name=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )

    llm_config = LLMConfig(
        model_name=os.getenv("LLM_MODEL", "llama3.2:3b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "512")),
    )

    vector_store_config = VectorStoreConfig(
        local_path=os.getenv("VECTOR_STORE_PATH", "health_supplements"),
        save_local=os.getenv("SAVE_VECTOR_STORE", "true").lower() == "true",
    )

    retrieval_config = RetrievalConfig(
        search_type=os.getenv("RETRIEVAL_TYPE", "mmr"),
        k=int(os.getenv("RETRIEVAL_K", "3")),
        fetch_k=int(os.getenv("RETRIEVAL_FETCH_K", "100")),
        lambda_mult=float(os.getenv("RETRIEVAL_LAMBDA", "1.0")),
    )

    doc_processing_config = DocumentProcessingConfig(
        chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "100")),
        dataset_path=os.getenv("DATASET_PATH", "rag-dataset"),
    )

    return AppConfig(
        embedding=embedding_config,
        llm=llm_config,
        vector_store=vector_store_config,
        retrieval=retrieval_config,
        document_processing=doc_processing_config,
    )


# Global configuration instance
config = load_config()
