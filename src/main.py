"""
Main application module for RAG PDF Chatbot.

This module provides the main entry point and CLI interface
for the RAG PDF Chatbot application.
"""

import os
import warnings

from src.config import config
from src.document_processor import DocumentProcessor
from src.rag_chain import RAGChain
from src.vector_store import VectorStoreManager

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")


class RAGPDFChatbot:
    """
    Main application class for RAG PDF Chatbot.

    This class orchestrates the entire RAG pipeline and provides
    a simple interface for question answering.
    """

    def __init__(self):
        """Initialize the RAG PDF Chatbot application."""
        self.document_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager()
        self.rag_chain = None

        # Set environment variable for KMP compatibility
        os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

    def initialize(self, rebuild_vector_store: bool = False) -> None:
        """
        Initialize the application and prepare for question answering.

        Args:
            rebuild_vector_store: Whether to rebuild vector store from scratch
        """
        # Check if vector store exists and load it if not rebuilding
        if not rebuild_vector_store and self.vector_store_manager.vector_store_exists():
            print("Loading existing vector store...")
            self.vector_store_manager.load_vector_store()
        else:
            print("Building vector store from documents...")
            documents = self.document_processor.process_documents()
            self.vector_store_manager.create_vector_store(documents)

            if config.vector_store.save_local:
                print("Saving vector store...")
                self.vector_store_manager.save_vector_store()

        # Initialize RAG chain
        retriever = self.vector_store_manager.get_retriever()
        self.rag_chain = RAGChain(retriever)

    def ask(self, question: str) -> str:
        """
        Ask a question using the RAG pipeline.

        Args:
            question: Question to answer

        Returns:
            str: Answer to the question
        """
        if not self.rag_chain:
            raise RuntimeError("Application not initialized. Call initialize() first.")

        return self.rag_chain.ask_question(question)

    def interactive_mode(self) -> None:
        """
        Run the application in interactive mode.

        Allows users to ask multiple questions in a session.
        """
        print("RAG PDF Chatbot - Interactive Mode")
        print("Type 'quit', 'exit', or 'q' to end the session.")
        print()

        while True:
            try:
                question = input("Ask a question: ").strip()

                if question.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break

                if not question:
                    continue

                print("Processing your question...")
                answer = self.ask(question)
                print("\nAnswer:")
                print(answer)
                print("\n" + "=" * 50 + "\n")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e!s}")
                continue


def main():
    """
    Main entry point for the RAG PDF Chatbot application.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="RAG PDF Chatbot - Retrieval-Augmented Generation for PDF documents"
    )
    parser.add_argument(
        "--rebuild", action="store_true", help="Rebuild vector store from scratch"
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument("--question", type=str, help="Ask a specific question")

    args = parser.parse_args()

    # Initialize application
    chatbot = RAGPDFChatbot()
    chatbot.initialize(rebuild_vector_store=args.rebuild)

    # Handle different modes
    if args.interactive:
        chatbot.interactive_mode()
    elif args.question:
        answer = chatbot.ask(args.question)
        print("Answer:")
        print(answer)
    else:
        print("RAG PDF Chatbot")
        print("Use --help for usage information")


if __name__ == "__main__":
    main()
