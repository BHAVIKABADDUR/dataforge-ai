# rag/retriever.py
# Retrieves relevant documentation chunks from FAISS vector store

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("rag/retailiq_index.faiss")

# Load chunks from pickle (matches what was indexed)
with open("rag/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


def retrieve(query, top_k=2):
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype="float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx])

    return results


if __name__ == "__main__":
    test_questions = [
        "What columns exist in dim_product?",
        "Explain the fact_sales table",
        "What customer information is stored?",
        "What region information exists?",
        "What date attributes are available?"
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        docs = retrieve(question)
        print("Retrieved:")
        for doc in docs:
            print("-" * 50)
            print(doc[:200])