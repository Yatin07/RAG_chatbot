"""
Document processing module for RAG PDF Chatbot.

This module handles loading, processing, and chunking of PDF documents
for the RAG pipeline.
"""

import os
import warnings
from typing import Any, Dict, List

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import config

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")


class DocumentProcessor:
    """
    Handles loading and processing of PDF documents.

    Responsibilities:
    - Discover PDF files in the dataset directory
    - Load PDF content using PyMuPDFLoader
    - Split documents into chunks for embedding
    """

    def __init__(self):
        """Initialize document processor with configuration."""
        self.dataset_path = config.document_processing.dataset_path
        self.chunk_size = config.document_processing.chunk_size
        self.chunk_overlap = config.document_processing.chunk_overlap

    def discover_pdf_files(self) -> List[str]:
        """
        Discover all PDF files in the dataset directory.

        Returns:
            List[str]: List of file paths to PDF documents
        """
        pdf_files = []

        for root, _, files in os.walk(self.dataset_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))

        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF files found in dataset directory: {self.dataset_path}"
            )

        return pdf_files

    def load_documents(self) -> List[Dict[str, Any]]:
        """
        Load all PDF documents from the dataset.

        Returns:
            List[Dict[str, Any]]: List of document objects
        """
        pdf_files = self.discover_pdf_files()
        documents = []

        for pdf_file in pdf_files:
            try:
                loader = PyMuPDFLoader(pdf_file)
                pages = loader.load()
                documents.extend(pages)
            except Exception as e:
                warnings.warn(f"Failed to load {pdf_file}: {e!s}", stacklevel=2)
                continue

        if not documents:
            raise RuntimeError("No documents were successfully loaded")

        return documents

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Split documents into chunks for embedding.

        Args:
            documents: List of document objects

        Returns:
            List[Dict[str, Any]]: List of document chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        return text_splitter.split_documents(documents)

    def process_documents(self) -> List[Dict[str, Any]]:
        """
        Complete document processing pipeline.

        Returns:
            List[Dict[str, Any]]: List of processed document chunks
        """
        documents = self.load_documents()
        return self.chunk_documents(documents)
