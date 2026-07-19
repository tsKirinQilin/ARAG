import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


load_dotenv()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


db = Chroma(
    persist_directory="knowledge/vector_db",
    embedding_function=embeddings
)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)


def decide_retrieval(question):
    """
    Decide whether external knowledge is needed.
    """

    prompt = f"""
You are a retrieval decision agent.

Decide if the user question requires information from a C# knowledge base.

Use RETRIEVE if:
- The question is about C# concepts.
- The answer may exist in the knowledge base.
- Documentation or examples are needed.

Use NO_RETRIEVE if:
- The question is general knowledge.
- The question does not relate to C#.

Return only one word:
RETRIEVE or NO_RETRIEVE


Question:
{question}
"""

    response = llm.invoke(prompt)

    decision = response.content.strip()

    return decision


def generate_answer(question, context=None):

    if context:
        prompt = f"""
You are a C# programming assistant.

Answer using only the provided context.

Context:

{context}


Question:

{question}
"""
    else:
        prompt = f"""
You are a helpful assistant.

Answer the question directly.

Question:

{question}
"""


    response = llm.invoke(prompt)

    return response.content



print("=" * 40)
print("C# AI Assistant")
print("Type 'exit' to quit")
print("=" * 40)


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break


    decision = decide_retrieval(question)


    print(f"\n[Agent decision: {decision}]")


    if decision == "RETRIEVE":

        docs = db.similarity_search(
            question,
            k=3
        )


        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        sources = [
            doc.metadata["source"] for doc in docs
        ]


        answer = generate_answer(
            question,
            context
        )


    else:

        answer = generate_answer(
            question
        )


    print("\nAI:")
    print(answer)

    if decision == "RETRIEVE":
        print("\nSources:")
        for source in sources:
            print("-", source)