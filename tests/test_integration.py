"""
Integration tests for RAG PDF Chatbot.

These tests verify that the major components work together correctly.
"""

import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from src.main import RAGPDFChatbot
from src.config import config

@patch('src.vector_store.VectorStoreManager')
@patch('src.document_processor.DocumentProcessor')
def test_chatbot_initialization(mock_doc_processor, mock_vector_store):
    """Test RAGPDFChatbot initialization."""
    # Setup mocks
    mock_doc_processor_instance = mock_doc_processor.return_value
    mock_vector_store_instance = mock_vector_store.return_value
    mock_vector_store_instance.vector_store_exists.return_value = False

    # Initialize chatbot
    chatbot = RAGPDFChatbot()

    # Verify components are initialized
    assert chatbot.document_processor == mock_doc_processor_instance
    assert chatbot.vector_store_manager == mock_vector_store_instance
    assert chatbot.rag_chain is None

@patch('src.vector_store.VectorStoreManager')
@patch('src.document_processor.DocumentProcessor')
def test_chatbot_initialize_with_existing_vector_store(mock_doc_processor, mock_vector_store):
    """Test chatbot initialization with existing vector store."""
    # Setup mocks
    mock_vector_store_instance = mock_vector_store.return_value
    mock_vector_store_instance.vector_store_exists.return_value = True
    mock_retriever = MagicMock()
    mock_vector_store_instance.get_retriever.return_value = mock_retriever

    # Initialize chatbot
    chatbot = RAGPDFChatbot()
    chatbot.initialize(rebuild_vector_store=False)

    # Verify vector store was loaded
    mock_vector_store_instance.load_vector_store.assert_called_once()
    mock_vector_store_instance.create_vector_store.assert_not_called()

    # Verify RAG chain was initialized
    assert chatbot.rag_chain is not None

@patch('src.vector_store.VectorStoreManager')
@patch('src.document_processor.DocumentProcessor')
def test_chatbot_initialize_with_new_vector_store(mock_doc_processor, mock_vector_store):
    """Test chatbot initialization with new vector store."""
    # Setup mocks
    mock_doc_processor_instance = mock_doc_processor.return_value
    mock_vector_store_instance = mock_vector_store.return_value
    mock_vector_store_instance.vector_store_exists.return_value = False

    mock_documents = [MagicMock(), MagicMock()]
    mock_doc_processor_instance.process_documents.return_value = mock_documents

    mock_retriever = MagicMock()
    mock_vector_store_instance.get_retriever.return_value = mock_retriever

    # Initialize chatbot
    chatbot = RAGPDFChatbot()
    chatbot.initialize(rebuild_vector_store=False)

    # Verify vector store was created
    mock_vector_store_instance.create_vector_store.assert_called_once_with(mock_documents)
    mock_vector_store_instance.load_vector_store.assert_not_called()

    # Verify RAG chain was initialized
    assert chatbot.rag_chain is not None

@patch('src.vector_store.VectorStoreManager')
@patch('src.document_processor.DocumentProcessor')
def test_chatbot_ask_question(mock_doc_processor, mock_vector_store):
    """Test chatbot question answering."""
    # Setup mocks
    mock_vector_store_instance = mock_vector_store.return_value
    mock_vector_store_instance.vector_store_exists.return_value = False

    mock_documents = [MagicMock()]
    mock_doc_processor.return_value.process_documents.return_value = mock_documents

    mock_retriever = MagicMock()
    mock_vector_store_instance.get_retriever.return_value = mock_retriever

    mock_rag_chain = MagicMock()
    mock_rag_chain.ask_question.return_value = "Test answer"

    # Mock RAGChain constructor
    with patch('src.main.RAGChain') as mock_rag_chain_class:
        mock_rag_chain_class.return_value = mock_rag_chain

        # Initialize chatbot
        chatbot = RAGPDFChatbot()
        chatbot.initialize(rebuild_vector_store=False)

        # Ask a question
        answer = chatbot.ask("Test question")

        # Verify answer
        assert answer == "Test answer"
        mock_rag_chain.ask_question.assert_called_once_with("Test question")

@patch('src.vector_store.VectorStoreManager')
@patch('src.document_processor.DocumentProcessor')
def test_chatbot_ask_before_initialization(mock_doc_processor, mock_vector_store):
    """Test asking question before initialization raises error."""
    # Initialize chatbot without calling initialize
    chatbot = RAGPDFChatbot()

    # Should raise error when asking question
    with pytest.raises(RuntimeError) as excinfo:
        chatbot.ask("Test question")

    assert "Application not initialized" in str(excinfo.value)

def test_chatbot_interactive_mode_mock():
    """Test interactive mode with mocked input."""
    # This is a basic test - in a real scenario, you'd want more comprehensive testing
    # of the interactive mode, possibly using a testing framework that can simulate
    # user input

    with patch('builtins.input', side_effect=['quit']):
        with patch('builtins.print') as mock_print:
            chatbot = RAGPDFChatbot()

            # Mock the initialize method to avoid dependencies
            with patch.object(chatbot, 'initialize'):
                chatbot.interactive_mode()

            # Verify it printed the welcome message
            calls = [str(call) for call in mock_print.call_args_list]
            welcome_msg = any("RAG PDF Chatbot - Interactive Mode" in str(call) for call in calls)
            assert welcome_msg is True
