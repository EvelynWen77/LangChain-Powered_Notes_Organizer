import os
from retriever.vector_store import build_faiss_index, save_faiss_index
from utils.note_loader import load_notes_as_documents

def main():
    print("📄 Loading notes from DB...")
    docs = load_notes_as_documents()

    if not docs:
        print("⚠️ No documents found. Please make sure your notes DB is not empty.")
        return

    print(f"🔢 Loaded {len(docs)} documents. Building FAISS index...")
    vectorstore = build_faiss_index(docs)

    print("💾 Saving FAISS index to ./data/faiss_index/")
    os.makedirs("./data/faiss_index", exist_ok=True)
    save_faiss_index(vectorstore)

    print("✅ Index build complete!")

if __name__ == "__main__":
    main()

# PYTHONPATH=. python scripts/build_index.py