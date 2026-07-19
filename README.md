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
