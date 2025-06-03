# 🧠 LangChain-Powered Notes Organizer

An AI-powered note management system built with LangChain agents, enabling structured classification, semantic search, and interactive querying of categorized notes using LLMs.

## 🔧 Features

- ✅ **LLM-based multi-tool agent** (ReAct framework)
- ✅ Extracts and classifies structured Q&A from raw text input
- ✅ Semantic search over historical notes using FAISS and OpenAI embeddings
- ✅ SQLite backend for metadata-driven filtering and retrieval
- ✅ Streamlit frontend for easy interaction and testing

## 📦 Tech Stack

- [LangChain](https://www.langchain.com/)
- [OpenAI API](https://platform.openai.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [SQLite](https://www.sqlite.org/index.html)
- [Streamlit](https://streamlit.io/)
- Python 3.11+

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Build FAISS index

```bash
python scripts/build_index.py
```

### 3. Run the app

```bash
streamlit run app.py
```

## 📁 Project Structure

```
.
├── app.py                   # Main Streamlit interface
├── agent_runner.py          # LangChain agent setup
├── retriever/               # FAISS + embeddings logic
├── utils/                   # Markdown export, classification, and DB logic
├── data/                    # SQLite DB and FAISS index
├── scripts/
│   └── build_index.py       # Build semantic vector index
└── requirements.txt
```

## 📌 Use Cases

- Personal AI-enhanced interview notes tracker
- Semantic Q&A memory system
- Lightweight RAG prototype

## 🧪 Example Query

> "What did company A ask me in round 2?"

The agent responds with questions, categories, and metadata from your stored notes.

## 📃 License

MIT License
