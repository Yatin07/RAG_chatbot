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

---

## Module 2: The Memory (Embeddings & FAISS)

**Q4: What is an embedding, and why do you need it?**
- **Model Answer:** "An embedding is a numerical representation of text—specifically a high-dimensional vector. Computers don't understand English natively. By converting text into vectors using the `nomic-embed-text` model, words or sentences that have similar semantic meaning are mapped physically close together in the vector space. This allows the system to search for meaning (e.g., 'dog' matches 'puppy') rather than just doing exact keyword matching."
- **Follow-up they might ask:** Why did you use Ollama for embeddings instead of OpenAI's `text-embedding-ada-002`?
  - *Answer:* Privacy and cost. Using Ollama keeps the entire process local. Enterprise clients often have strict data privacy policies (like HIPAA or GDPR), meaning they cannot legally send their sensitive PDF documents to an external API like OpenAI.

**Q5: You used FAISS for your vector database. Why FAISS over Pinecone or ChromaDB?**
- **Model Answer:** "I chose FAISS (Facebook AI Similarity Search) because it is highly optimized for in-memory, local operations. Unlike Pinecone, it doesn't require cloud infrastructure or network calls, making it incredibly fast and perfect for a fully local architecture. It handles L2 distance calculations efficiently using highly optimized C++ under the hood."
- **Follow-up they might ask:** What happens if the FAISS index gets too big to fit in RAM?
  - *Answer:* FAISS is primarily an in-memory store. If the dataset scales to millions of documents that exceed system RAM, I would need to migrate to a disk-based vector database like Qdrant or Milvus, or use FAISS's disk-backed indexing options.

**Q6: What search algorithm are you using during retrieval, and why did you configure `k=3`?**
- **Model Answer:** "I retrieve the top 3 chunks (`k=3`) because sending too many chunks to the LLM pollutes the prompt and dilutes the context, while sending too few might miss the answer. More importantly, I use **MMR (Maximal Marginal Relevance)** instead of basic similarity search. MMR ensures that the 3 chunks I fetch are highly relevant to the query, but also diverse from one another. This prevents the database from returning 3 chunks that all say the exact same thing."
- **Follow-up they might ask:** How exactly does FAISS mathematically determine similarity?
  - *Answer:* In my implementation, it uses `IndexFlatL2`, which calculates the Euclidean distance (the straight-line mathematical distance) between the vectors. The smaller the distance, the more similar the semantic meaning.

---

## Module 3: The Brain (RAG & LangChain)

**Q7: Can you walk me through your LCEL (LangChain Expression Language) pipeline? What is actually happening in your code?**
- **Model Answer:** "My RAG chain is built using LCEL's pipe syntax. It starts by taking a dictionary containing the user's question and the context. The context is fetched by piping the question into the FAISS retriever, and the question is passed through using `RunnablePassthrough`. These two variables are piped into a `ChatPromptTemplate`, which structures the final prompt. That prompt is piped into `ChatOllama` (the LLM) for inference, and the raw output object is finally piped into a `StrOutputParser` to extract a clean string for the user."
- **Follow-up they might ask:** Why use LCEL instead of just writing standard Python functions to pass the data?
  - *Answer:* LCEL provides built-in streaming, asynchronous support, and tracing out of the box. Writing it via the `|` pipe operator creates a highly readable, standardized graph that LangChain can easily optimize under the hood.

**Q8: In your prompt template, you explicitly tell the LLM: 'Use the following pieces of retrieved context to answer the question.' Why is this necessary?**
- **Model Answer:** "This is the fundamental principle of RAG (Retrieval-Augmented Generation). LLMs are trained to hallucinate—they predict the most probable next word based on their massive training dataset. If I don't strictly bind the LLM to the provided context, it might confidently generate an answer based on its pre-existing knowledge (which might be outdated or factually wrong for our specific PDFs). By explicitly instructing it to use the context, I anchor its generation to facts retrieved from my database."
- **Follow-up they might ask:** What if the FAISS database returns irrelevant context?
  - *Answer:* The LLM will likely get confused and answer based on the irrelevant context, or hallucinate. This is why tuning the retrieval (like using MMR, adjusting chunk size, and setting a solid `k` value) is arguably more important than the LLM itself in a production RAG system.

**Q9: Why did you set the temperature of your LLM to 0.7?**
- **Model Answer:** "Temperature dictates the randomness of the token prediction. A temperature of 0.0 forces the model to act completely deterministically, choosing the highest probability word every single time. A temperature of 1.0 makes it highly creative but prone to hallucination. For a RAG system, 0.7 is a standard middle-ground that allows the LLM to weave the retrieved facts into a fluent, conversational answer without deviating too far into hallucination."

---

## Module 4: The Orchestration

**Q10: In your `main.py`, you have a `--rebuild` flag. Why is this necessary?**
- **Model Answer:** "Embedding documents and building a vector database is computationally expensive and slow. To optimize startup time, my application saves the FAISS index to the local disk. When the app starts, it checks if the index exists and loads it into memory instantly. The `--rebuild` flag gives the user a manual override to force the system to re-read the PDFs and re-embed everything, which is necessary if they added new PDFs to the `rag-dataset/` folder."
- **Follow-up they might ask:** Could you automate the rebuild process instead of relying on a manual flag?
  - *Answer:* Yes. I could implement a hashing mechanism that calculates the MD5 hash of the `rag-dataset/` folder. On startup, the app would compare the current hash to the saved hash. If they don't match, it means a PDF was added, modified, or deleted, and the app would trigger a rebuild automatically.

**Q11: How do you prevent your application from immediately closing after answering one question?**
- **Model Answer:** "I implemented an `interactive_mode` function that uses an infinite `while True:` loop. The loop calls Python's built-in `input()` function, which halts execution and waits for the user's terminal input. Once the LLM answers, the loop restarts. It only terminates if the user types a specific exit command (like 'quit') which triggers a `break` statement."
- **Follow-up they might ask:** What happens if the user presses `Ctrl+C` in the terminal during the interactive loop?
  - *Answer:* That sends a `KeyboardInterrupt` signal to Python, which would normally crash the program and print a massive, ugly stack trace. I wrapped the input loop in a `try/except KeyboardInterrupt:` block to catch that specific signal and exit gracefully with a 'Goodbye!' message instead of crashing.
