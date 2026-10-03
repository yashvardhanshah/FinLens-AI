import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


def build_vectorstore(uploaded_file):
    """
    Takes an uploaded PDF, chunks it, embeds it,
    stores in FAISS and returns the vectorstore.
    """
    # Save uploaded file temporarily to disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(uploaded_file.getvalue())
        tmp_path = f.name

    # Extract text from PDF page by page
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    # Split into 500-word chunks with 50-word overlap
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    # Convert chunks to vectors using HuggingFace embeddings
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # Store all vectors in FAISS
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Delete temp file
    os.unlink(tmp_path)

    return vectorstore


def search_vectorstore(vectorstore, query, k=4):
    """
    Searches FAISS for the most relevant chunks to the query.
    Returns top k chunks as a single string.
    """
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])