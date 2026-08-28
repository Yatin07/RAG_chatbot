"""
Unit tests for the config module.
"""

import os
import tempfile
from unittest.mock import patch
import pytest
from src.config import (
    EmbeddingConfig,
    LLMConfig,
    VectorStoreConfig,
    RetrievalConfig,
    DocumentProcessingConfig,
    AppConfig,
    load_config,
    config,
)

def test_embedding_config_defaults():
    """Test EmbeddingConfig with default values."""
    embedding_config = EmbeddingConfig()
    assert embedding_config.model_name == "nomic-embed-text"
    assert embedding_config.base_url == "http://localhost:11434"
    assert embedding_config.dimension is None

def test_llm_config_defaults():
    """Test LLMConfig with default values."""
    llm_config = LLMConfig()
    assert llm_config.model_name == "llama3.2:3b"
    assert llm_config.base_url == "http://localhost:11434"
    assert llm_config.temperature == 0.7
    assert llm_config.max_tokens == 512

def test_vector_store_config_defaults():
    """Test VectorStoreConfig with default values."""
    vector_config = VectorStoreConfig()
    assert vector_config.index_type == "flat"
    assert vector_config.metric == "L2"
    assert vector_config.save_local is True
    assert vector_config.local_path == "health_supplements"

def test_retrieval_config_defaults():
    """Test RetrievalConfig with default values."""
    retrieval_config = RetrievalConfig()
    assert retrieval_config.search_type == "mmr"
    assert retrieval_config.k == 3
    assert retrieval_config.fetch_k == 100
    assert retrieval_config.lambda_mult == 1.0

def test_document_processing_config_defaults():
    """Test DocumentProcessingConfig with default values."""
    doc_config = DocumentProcessingConfig()
    assert doc_config.chunk_size == 1000
    assert doc_config.chunk_overlap == 100
    assert doc_config.dataset_path == "rag-dataset"

def test_app_config_structure():
    """Test AppConfig structure."""
    app_config = AppConfig(
        embedding=EmbeddingConfig(),
        llm=LLMConfig(),
        vector_store=VectorStoreConfig(),
        retrieval=RetrievalConfig(),
        document_processing=DocumentProcessingConfig()
    )
    assert isinstance(app_config.embedding, EmbeddingConfig)
    assert isinstance(app_config.llm, LLMConfig)
    assert isinstance(app_config.vector_store, VectorStoreConfig)
    assert isinstance(app_config.retrieval, RetrievalConfig)
    assert isinstance(app_config.document_processing, DocumentProcessingConfig)

@patch.dict(os.environ, {
    "EMBEDDING_MODEL": "custom-embedding",
    "OLLAMA_BASE_URL": "http://custom-ollama:11434",
    "LLM_MODEL": "custom-llm",
    "LLM_TEMPERATURE": "0.5",
    "LLM_MAX_TOKENS": "256",
    "VECTOR_STORE_PATH": "custom-vector-store",
    "SAVE_VECTOR_STORE": "false",
    "RETRIEVAL_TYPE": "similarity",
    "RETRIEVAL_K": "5",
    "RETRIEVAL_FETCH_K": "50",
    "RETRIEVAL_LAMBDA": "0.5",
    "CHUNK_SIZE": "500",
    "CHUNK_OVERLAP": "50",
    "DATASET_PATH": "custom-dataset"
})
def test_load_config_from_environment():
    """Test loading configuration from environment variables."""
    # Reload config to pick up environment variables
    test_config = load_config()

    # Test embedding config
    assert test_config.embedding.model_name == "custom-embedding"
    assert test_config.embedding.base_url == "http://custom-ollama:11434"

    # Test LLM config
    assert test_config.llm.model_name == "custom-llm"
    assert test_config.llm.temperature == 0.5
    assert test_config.llm.max_tokens == 256

    # Test vector store config
    assert test_config.vector_store.local_path == "custom-vector-store"
    assert test_config.vector_store.save_local is False

    # Test retrieval config
    assert test_config.retrieval.search_type == "similarity"
    assert test_config.retrieval.k == 5
    assert test_config.retrieval.fetch_k == 50
    assert test_config.retrieval.lambda_mult == 0.5

    # Test document processing config
    assert test_config.document_processing.chunk_size == 500
    assert test_config.document_processing.chunk_overlap == 50
    assert test_config.document_processing.dataset_path == "custom-dataset"

def test_load_config_with_missing_env_vars():
    """Test loading configuration with missing environment variables."""
    # Clear environment variables
    for key in [
        "EMBEDDING_MODEL", "OLLAMA_BASE_URL", "LLM_MODEL", "LLM_TEMPERATURE",
        "LLM_MAX_TOKENS", "VECTOR_STORE_PATH", "SAVE_VECTOR_STORE",
        "RETRIEVAL_TYPE", "RETRIEVAL_K", "RETRIEVAL_FETCH_K", "RETRIEVAL_LAMBDA",
        "CHUNK_SIZE", "CHUNK_OVERLAP", "DATASET_PATH"
    ]:
        if key in os.environ:
            del os.environ[key]

    # Load config should use defaults
    test_config = load_config()

    # Test that defaults are used
    assert test_config.embedding.model_name == "nomic-embed-text"
    assert test_config.llm.model_name == "llama3.2:3b"
    assert test_config.vector_store.local_path == "health_supplements"
    assert test_config.retrieval.search_type == "mmr"
    assert test_config.document_processing.dataset_path == "rag-dataset"

def test_config_global_instance():
    """Test that global config instance is properly initialized."""
    assert isinstance(config, AppConfig)
    assert isinstance(config.embedding, EmbeddingConfig)
    assert isinstance(config.llm, LLMConfig)
    assert isinstance(config.vector_store, VectorStoreConfig)
    assert isinstance(config.retrieval, RetrievalConfig)
    assert isinstance(config.document_processing, DocumentProcessingConfig)

def test_config_immutability():
    """Test that config instances are immutable where appropriate."""
    embedding_config = EmbeddingConfig()
    with pytest.raises(Exception):  # dataclasses are immutable by default
        embedding_config.model_name = "new-model"
