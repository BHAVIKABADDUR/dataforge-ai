# rag/build_vector_store.py
# Builds FAISS vector store from RetailIQ schema documentation

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load documentation
with open("knowledge_base/retailiq_schema.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split on TABLE: — one chunk per table
raw_chunks = text.split("TABLE:")
chunks = []
for chunk in raw_chunks:
    chunk = chunk.strip()
    if chunk:
        chunks.append("TABLE: " + chunk)

print(f"Chunks created: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---")
    print(chunk[:100])

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(chunks)
embeddings = np.array(embeddings, dtype="float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, "rag/retailiq_index.faiss")

# Save chunks separately so retriever can return text
with open("rag/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("\nVector store created successfully")
print(f"Total chunks indexed: {len(chunks)}")