"""
Test package for RAG PDF Chatbot.

This package contains unit and integration tests for all components
of the RAG PDF Chatbot application.
"""

import os
import sys

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Mock environment variables for testing
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"
os.environ["EMBEDDING_MODEL"] = "test-model"
os.environ["LLM_MODEL"] = "test-llm"
os.environ["DATASET_PATH"] = "tests/test-data"
os.environ["VECTOR_STORE_PATH"] = "tests/test-vector-store"
os.environ["SAVE_VECTOR_STORE"] = "false"
