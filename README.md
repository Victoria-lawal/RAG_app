# RAG App — AI Engineer

A Retrieval-Augmented Generation (RAG) app that answers questions from a document using ChromaDB and Mistral.

## Files

- `app.py` — sanity check that your Mistral API connection works
- `ingest.py` — loads your document, splits it into chunks, stores them in ChromaDB
- `query.py` — takes a question, finds the relevant chunk, sends it to Mistral for an answer

## Setup

```bash
pip install chromadb mistralai python-dotenv
```

Create a `.env` file:

```
MISTRAL_API_KEY=your_key_here
```

## How to run

Run once to load your document:

```bash
python ingest.py
```

Then ask questions:

```bash
python query.py
```

## How it works

1. `ingest.py` reads your `.txt` file, splits it into 500-word chunks, and stores them in a local ChromaDB database (`./db`)
2. `query.py` takes your question, finds the most similar chunk in ChromaDB, and sends that chunk + question to Mistral
3. Mistral answers based only on the retrieved chunk

## .gitignore

Make sure your `.gitignore` includes:

```
.env
./db
```
