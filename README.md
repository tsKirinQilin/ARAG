# Agentic RAG Assistant

This project is an Agentic RAG assistant that answers C# questions using my own knowledge base.

Unlike a basic RAG system, the assistant first decides whether it needs to retrieve information from the knowledge base or answer directly.

## How it works

The workflow:

User question → Retrieval decision → (Retrieve from ChromaDB or answer directly) → LLM response

The agent makes one autonomous decision:

RETRIEVE:
The assistant searches the C# knowledge base and uses the found information to generate an answer.

NO_RETRIEVE:
The assistant answers directly without using the vector database.

## Tech Stack

LLM:
- Groq API (Llama 3.1 8B Instant)

Embeddings:
- sentence-transformers/all-MiniLM-L6-v2

Vector database:
- ChromaDB

Framework:
- LangChain

## Knowledge Base

I created a small C# knowledge base with 10 documents:

- Variables
- Conditions
- Loops
- Methods
- OOP
- Inheritance
- Interfaces
- Collections
- LINQ
- JSON

The documents are converted into embeddings and stored in ChromaDB.

## Running the project

Install dependencies:

pip install -r requirements.txt

Create vector database:

python create_vector_db.py

Run assistant:

python rag_assistant.py

## Failure Case

During testing, I asked:

"How does inheritance work in C#?"

Sometimes the retriever returned unrelated C# documents instead of the inheritance document.

The reason was a small knowledge base and simple embedding search. The system recognized the topic as C#, but could not always find the most specific document.

Possible improvements:

- Add more documents
- Improve chunking
- Use a stronger embedding model

Built an Agentic RAG assistant that answers C# questions using basic knowledge base.

Unlike a basic RAG system, it has an autonomous retrieval decision step. Before searching the vector database, the agent decides whether retrieval is needed. If the question is related to the C# knowledge base, it chooses RETRIEVE and searches ChromaDB. Otherwise, it chooses NO_RETRIEVE and answers directly without retrieval. This decision changes the behavior of the system.

The answers are grounded and traceable because when retrieval is used, the assistant generates responses from retrieved knowledge base documents and shows the source files used for the answer.

The retrieval process is based on semantic similarity search. User questions and documents are converted into embeddings using sentence-transformers, and ChromaDB returns the most relevant document chunks.

During testing, I found a failure case where a question about a specific C# topic sometimes retrieved general C# documents instead of the exact topic document. I diagnosed that the issue was caused by a small knowledge base and simple embedding similarity search. Possible improvements would be adding more documents, improving chunking, or using a stronger embedding model.
