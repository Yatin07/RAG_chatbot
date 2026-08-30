"""
Unit tests for the document processor module.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.config import config
from src.document_processor import DocumentProcessor


def test_document_processor_initialization():
    """Test DocumentProcessor initialization."""
    processor = DocumentProcessor()
    assert processor.dataset_path == config.document_processing.dataset_path
    assert processor.chunk_size == config.document_processing.chunk_size
    assert processor.chunk_overlap == config.document_processing.chunk_overlap


@patch("os.walk")
@patch("src.document_processor.PyMuPDFLoader")
def test_discover_pdf_files(mock_loader, mock_walk):
    """Test PDF file discovery."""
    # Setup mock file structure
    mock_walk.return_value = [
        ("tests/test-data", ["subdir"], ["test1.pdf", "test2.txt", "test3.pdf"]),
        ("tests/test-data/subdir", [], ["test4.pdf", "test5.doc"]),
    ]

    processor = DocumentProcessor()
    pdf_files = processor.discover_pdf_files()

    # Should find 3 PDF files
    assert len(pdf_files) == 3
    assert "tests/test-data/test1.pdf" in pdf_files
    assert "tests/test-data/test3.pdf" in pdf_files
    assert "tests/test-data/subdir/test4.pdf" in pdf_files
    assert "tests/test-data/test2.txt" not in pdf_files
    assert "tests/test-data/subdir/test5.doc" not in pdf_files


@patch("os.walk")
def test_discover_pdf_files_no_pdfs(mock_walk):
    """Test PDF file discovery when no PDFs are found."""
    # Setup mock file structure with no PDFs
    mock_walk.return_value = [
        ("tests/test-data", [], ["test1.txt", "test2.doc"]),
    ]

    processor = DocumentProcessor()

    with pytest.raises(FileNotFoundError) as excinfo:
        processor.discover_pdf_files()

    assert "No PDF files found in dataset directory" in str(excinfo.value)


@patch("src.document_processor.PyMuPDFLoader")
def test_load_documents(mock_loader):
    """Test document loading."""
    # Setup mock loader
    mock_pages = [
        MagicMock(
            page_content="Page 1 content", metadata={"source": "test.pdf", "page": 1}
        ),
        MagicMock(
            page_content="Page 2 content", metadata={"source": "test.pdf", "page": 2}
        ),
    ]
    mock_loader.return_value.load.return_value = mock_pages

    processor = DocumentProcessor()

    with patch.object(processor, "discover_pdf_files") as mock_discover:
        mock_discover.return_value = ["test.pdf"]
        documents = processor.load_documents()

    assert len(documents) == 2
    assert documents[0].page_content == "Page 1 content"
    assert documents[1].page_content == "Page 2 content"


@patch("src.document_processor.PyMuPDFLoader")
def test_load_documents_with_error(mock_loader):
    """Test document loading with error handling."""
    # Setup mock loader to raise exception
    mock_loader.return_value.load.side_effect = Exception("Test error")

    processor = DocumentProcessor()

    with patch.object(processor, "discover_pdf_files") as mock_discover:
        mock_discover.return_value = ["test.pdf", "test2.pdf"]

        # Mock the second loader to work
        def side_effect(file):
            if file == "test.pdf":
                raise Exception("Test error")
            return [MagicMock(page_content="Working content", metadata={})]

        mock_loader.return_value.load.side_effect = side_effect

        documents = processor.load_documents()

    assert len(documents) == 1
    assert documents[0].page_content == "Working content"


@patch("src.document_processor.PyMuPDFLoader")
def test_load_documents_all_fail(mock_loader):
    """Test document loading when all files fail."""
    # Setup mock loader to always raise exception
    mock_loader.return_value.load.side_effect = Exception("Test error")

    processor = DocumentProcessor()

    with patch.object(processor, "discover_pdf_files") as mock_discover:
        mock_discover.return_value = ["test.pdf"]

        with pytest.raises(RuntimeError) as excinfo:
            processor.load_documents()

        assert "No documents were successfully loaded" in str(excinfo.value)


@patch("src.document_processor.RecursiveCharacterTextSplitter")
@patch("src.document_processor.PyMuPDFLoader")
def test_chunk_documents(mock_loader, mock_splitter):
    """Test document chunking."""
    # Setup mock documents
    mock_documents = [
        MagicMock(page_content="Document 1 content", metadata={}),
        MagicMock(page_content="Document 2 content", metadata={}),
    ]

    # Setup mock splitter
    mock_chunks = [
        MagicMock(page_content="Chunk 1", metadata={}),
        MagicMock(page_content="Chunk 2", metadata={}),
        MagicMock(page_content="Chunk 3", metadata={}),
    ]
    mock_splitter.return_value.split_documents.return_value = mock_chunks

    processor = DocumentProcessor()
    chunks = processor.chunk_documents(mock_documents)

    assert len(chunks) == 3
    assert chunks == mock_chunks

    # Verify splitter was called with correct parameters
    mock_splitter.assert_called_once()
    splitter_instance = mock_splitter.return_value
    splitter_instance.split_documents.assert_called_once_with(mock_documents)


@patch("src.document_processor.RecursiveCharacterTextSplitter")
@patch("src.document_processor.PyMuPDFLoader")
def test_process_documents(mock_loader, mock_splitter):
    """Test complete document processing pipeline."""
    # Setup mock documents and chunks
    mock_documents = [MagicMock(page_content="Doc content", metadata={})]
    mock_chunks = [MagicMock(page_content="Chunk content", metadata={})]

    mock_loader.return_value.load.return_value = mock_documents
    mock_splitter.return_value.split_documents.return_value = mock_chunks

    processor = DocumentProcessor()

    with patch.object(processor, "discover_pdf_files") as mock_discover:
        mock_discover.return_value = ["test.pdf"]
        chunks = processor.process_documents()

    assert len(chunks) == 1
    assert chunks == mock_chunks
