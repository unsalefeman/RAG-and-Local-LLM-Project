# RAG-and-Local-LLM-Project
# Local RAG Assistant (Foundry Local)

A fully offline document Q&A assistant built with Microsoft Foundry Local.
It answers questions using Retrieval-Augmented Generation (RAG) — retrieving
relevant passages from a local document (Thomas' Calculus) and using a local
LLM (phi-3.5-mini) to generate grounded answers, entirely on-device with no
internet connection required.

## How it works

1. **Ingestion** (`ingest.py`) — reads PDF/TXT files from `data/`, splits them
   into sentence-aware chunks, generates embeddings with Foundry Local's
   `qwen3-embedding-0.6b` model, and stores everything in a local SQLite
   database (`rag.db`).
2. **Retrieval** (`retrieval.py`) — embeds a user's question and finds the
   most similar chunks in the database using cosine similarity.
3. **Answer generation** (`qa.py`) — combines the retrieved chunks with the
   question into a prompt, sends it to `phi-3.5-mini` via Foundry Local's
   chat client, and streams back a grounded answer.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Place your source documents (`.txt` or `.pdf`) in the `data/` folder.
2. Run ingestion (add `--reset` to rebuild the database from scratch):
```bash
   python ingest.py --reset
```
3. Start the assistant:
```bash
   python qa.py
```
4. Ask questions in the terminal. Type `q` to quit.

## Design decisions

- **Chunking:** sentence-aware splitting (150–500 characters) to avoid
  cutting sentences mid-way and to keep chunks topically focused.
- **Models:** `qwen3-embedding-0.6b` for embeddings (fast, small) and
  `phi-3.5-mini` for chat (balance of speed and answer quality on CPU).
- **Storage:** SQLite chosen for simplicity — a single-file database with
  no server setup, suitable for this project's scale (thousands of chunks).
- **System prompt:** instructs the model to answer only from retrieved
  context and to admit when information is missing, reducing hallucination.

## Known limitations

- Retrieval occasionally returns semantically similar but topically
  different content for ambiguous queries.
- The model may fall back on general knowledge for very simple reasoning
  tasks despite prompt instructions.
- Not designed for reliable multi-step mathematical computation — the
  system retrieves explanatory text, but calculations are performed by the
  LLM itself and are not guaranteed to be accurate for complex problems.
