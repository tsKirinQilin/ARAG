# Agentic RAG Assistant

An Agentic RAG assistant that answers C# programming questions using a custom knowledge base.

The project uses retrieval-augmented generation with an additional autonomous retrieval decision step. Before answering, the agent decides whether external knowledge retrieval is required.

## Project Overview

The assistant combines:

* A Large Language Model (Groq Llama)
* A custom C# knowledge base
* Embeddings for semantic search
* Chroma vector database
* An autonomous retrieval decision agent

Unlike a basic RAG system, this assistant does not always retrieve documents. It first decides whether retrieval is useful.

## Tech Stack

### LLM

* Groq API
* Llama 3.1 8B Instant

### Embeddings

* sentence-transformers/all-MiniLM-L6-v2

### Vector Database

* ChromaDB

### Frameworks and Libraries

* LangChain
* LangChain Groq
* LangChain Chroma
* LangChain HuggingFace
* Python

## Knowledge Base

The knowledge base contains custom C# learning documents:

```
knowledge/
│
├── 01_variables.txt
├── 02_conditions.txt
├── 03_loops.txt
├── 04_methods.txt
├── 05_oop.txt
├── 06_inheritance.txt
├── 07_interfaces.txt
├── 08_collections.txt
├── 09_linq.txt
└── 10_json.txt
```

The documents are split into smaller chunks and converted into embeddings before being stored in ChromaDB.

## Agentic Decision

The main agentic behavior is the retrieval decision step.

Before answering a question, the assistant asks a decision model:

```
Does this question require information from the C# knowledge base?
```

The agent returns one of two decisions:

```
RETRIEVE
```

or

```
NO_RETRIEVE
```

## Agent Behavior Example

### Example 1: Retrieval Required

User:

```
What is inheritance in C#?
```

Agent decision:

```
RETRIEVE
```

Flow:

```
Question
   ↓
Retrieval decision
   ↓
Chroma similarity search
   ↓
Relevant C# documents
   ↓
LLM answer
```

### Example 2: Retrieval Not Required

User:

```
What is the capital of Japan?
```

Agent decision:

```
NO_RETRIEVE
```

Flow:

```
Question
   ↓
Retrieval decision
   ↓
Direct LLM answer
```

The system avoids unnecessary vector database searches.

## Project Structure

```
AgenticRAGAssistant/

├── knowledge/
│   ├── *.txt
│   └── vector_db/
│
├── create_vector_db.py
├── rag_assistant.py
├── requirements.txt
├── README.md
└── .env
```

## How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Create vector database

Run:

```
python create_vector_db.py
```

This creates embeddings and stores them in ChromaDB.

### 3. Start the assistant

Run:

```
python rag_assistant.py
```

Example:

```
You: Explain JSON serialization in C#

[Agent decision: RETRIEVE]

AI:
JSON serialization converts objects into JSON format...

Sources:
- knowledge\10_json.txt
```

## Failure Case

### Problem

Question:

```
How does inheritance work in C#?
```

Expected behavior:

The retriever should return:

```
knowledge/06_inheritance.txt
```

Actual behavior:

The retriever returned unrelated C# documents such as:

```
knowledge/01_variables.txt
knowledge/02_conditions.txt
```

## Diagnosis

The issue was caused by:

* Small knowledge base size
* Short document chunks
* Embedding similarity matching general C# concepts instead of the exact topic

The retriever recognized that the documents were related to C#, but not the specific concept requested.

## Improvements

Possible improvements:

* Add more detailed knowledge documents
* Tune chunk size and overlap
* Use a stronger embedding model
* Add retrieval quality evaluation
* Add query rewriting before retrieval

## Limitations

Current limitations:

* The knowledge base is small
* Retrieval quality depends on embedding similarity
* The decision agent can occasionally choose an incorrect retrieval strategy

Despite these limitations, the system demonstrates autonomous retrieval control and grounded generation.
