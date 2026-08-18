"""
RAG chain module for RAG PDF Chatbot.

This module implements the Retrieval-Augmented Generation pipeline
for question answering using retrieved document context.
"""

import warnings
from typing import Dict, Any, Optional
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from src.config import config

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

class RAGChain:
    """
    Implements the RAG (Retrieval-Augmented Generation) pipeline.

    Responsibilities:
    - Initialize LLM model
    - Create prompt templates
    - Build RAG chain pipeline
    - Handle question answering
    """

    def __init__(self, retriever: Any):
        """
        Initialize RAG chain with retriever.

        Args:
            retriever: Document retriever object
        """
        self.retriever = retriever
        self.llm = self._initialize_llm()
        self.prompt = self._create_prompt()
        self.chain = self._build_chain()

    def _initialize_llm(self) -> ChatOllama:
        """
        Initialize the LLM model.

        Returns:
            ChatOllama: Configured LLM model
        """
        return ChatOllama(
            model=config.llm.model_name,
            base_url=config.llm.base_url,
            temperature=config.llm.temperature
        )

    def _create_prompt(self) -> ChatPromptTemplate:
        """
        Create the prompt template for RAG.

        Returns:
            ChatPromptTemplate: Configured prompt template
        """
        # Try to load from hub first, fall back to custom template
        try:
            prompt = hub.pull("rlm/rag-prompt")
        except Exception:
            # Custom RAG prompt template
            template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.

If possible answer in bullet points. Make sure your answer is relevant to the question and it is answered from the context only.

Question:{question}

Context:{context}

Answer:
"""
            prompt = ChatPromptTemplate.from_template(template)

        return prompt

    def _build_chain(self) -> Any:
        """
        Build the RAG chain pipeline.

        Returns:
            Any: Configured RAG chain
        """
        def format_docs(docs: List[Dict[str, Any]]) -> str:
            """Format retrieved documents for context."""
            return "\n\n".join([doc.page_content for doc in docs])

        return (
            {
                "context": self.retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask_question(self, question: str) -> str:
        """
        Ask a question using the RAG pipeline.

        Args:
            question: Question to answer

        Returns:
            str: Answer to the question
        """
        if not self.chain:
            raise RuntimeError("RAG chain not initialized")

        return self.chain.invoke(question)

    def get_chain(self) -> Any:
        """
        Get the RAG chain object.

        Returns:
            Any: RAG chain object
        """
        return self.chain
