"""
RAG PDF Chatbot - A Retrieval-Augmented Generation system for PDF documents.

This package provides a modular, enterprise-grade implementation of RAG
for question answering using PDF document collections.
"""

from .config import config, load_config
from .document_processor import DocumentProcessor
from .vector_store import VectorStoreManager
from .rag_chain import RAGChain
from .main import RAGPDFChatbot, main

__version__ = "1.0.0"
__author__ = "RAG PDF Chatbot Team"
__license__ = "MIT"
__all__ = [
    "config",
    "load_config",
    "DocumentProcessor",
    "VectorStoreManager",
    "RAGChain",
    "RAGPDFChatbot",
    "main"
]
