# Interview Q&A Cheat Sheet

This document contains a curated list of potential interview questions and perfect answers based on the concepts covered in the teaching plan.

---

## Module 1: Document Processing

**Q1: How does your RAG system handle large PDFs without exceeding the LLM's context window?**
- **Model Answer:** "I process the PDFs in two steps. First, I extract the text using `PyMuPDFLoader`. Then, because LLMs have strict memory limits, I pass the raw text through a `RecursiveCharacterTextSplitter` to break the document into digestible chunks of 1000 characters before sending them to the vector database."
- **Follow-up they might ask:** Why didn't you just split the text every 1000 characters using a standard Python string slice (`text[:1000]`)?
  - *Answer:* A hard slice would randomly cut words or sentences in half, completely destroying the semantic meaning. The `RecursiveCharacterTextSplitter` intelligently tries to split at natural boundaries like paragraphs and sentences first, only splitting mid-sentence if absolutely necessary.

**Q2: In your text splitting logic, you configured a `chunk_overlap` of 100. What is the exact mathematical or logical purpose of this?**
- **Model Answer:** "Chunk overlap prevents context loss at the boundaries. If a critical concept is being explained right at the 1000-character mark, chunking without overlap splits that thought across two separate database entries. By overlapping 100 characters, the end of Chunk A is duplicated at the beginning of Chunk B, ensuring the LLM always has the full surrounding context to generate an accurate answer."
- **Follow-up they might ask:** What happens if your `chunk_size` is too small (e.g., 50 characters)?
  - *Answer:* The chunks become too fragmented. The vector database might successfully retrieve an isolated phrase like "the company profits grew," but without the surrounding sentences, the LLM won't know *which* company or *why* they grew, leading to severe AI hallucinations.

**Q3: Which library did you use for PDF extraction and why?**
- **Model Answer:** "I used LangChain's integration with `PyMuPDF`. During my research, I found that PyMuPDF is much faster and handles complex layouts, embedded fonts, and weirdly formatted PDF columns much better than older libraries like PyPDF2."
- **Follow-up they might ask:** Does this system handle images or charts inside the PDF?
  - *Answer:* In this specific architecture, no. PyMuPDFLoader extracts text, but images are ignored. To handle images, I would need to upgrade the pipeline to a Multi-modal RAG system using OCR (Optical Character Recognition) or a Vision-Language Model like LLaVA.
