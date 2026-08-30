"""
RAG PDF Chatbot - A Retrieval-Augmented Generation system for PDF documents.

This package provides a modular, enterprise-grade implementation of RAG
for question answering using PDF document collections.
"""

from .config import config, load_config
from .document_processor import DocumentProcessor
from .main import RAGPDFChatbot, main
from .rag_chain import RAGChain
from .vector_store import VectorStoreManager

__version__ = "1.0.0"
__author__ = "RAG PDF Chatbot Team"
__license__ = "MIT"
__all__ = [
    "DocumentProcessor",
    "RAGChain",
    "RAGPDFChatbot",
    "VectorStoreManager",
    "config",
    "load_config",
    "main",
]
