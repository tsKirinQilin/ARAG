from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

import glob



documents = []

files = glob.glob("knowledge/*.txt")


for file in files:
    loader = TextLoader(
        file,
        encoding="utf-8"
    )

    documents.extend(loader.load())


print("Документов:", len(documents))



splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)


chunks = splitter.split_documents(documents)


print("Chunks:", len(chunks))



embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="knowledge/vector_db"
)


print("Vector DB создана!")