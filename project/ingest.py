import argparse
import glob
import os
import re
from database import clear_documents, get_all_documents, init_db, insert_document
from foundry_local_sdk import Configuration, FoundryLocalManager
from pypdf import PdfReader


DATA_DIR = "data"


def clean_pdf_text(text):
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]+", " ", text)
    return text


def clean_gutenberg_text(text):
    start_match = re.search(r"\*\*\* START OF.*?\*\*\*", text, re.IGNORECASE)
    end_match = re.search(r"\*\*\* END OF.*?\*\*\*", text, re.IGNORECASE)

    if start_match:
        text = text[start_match.end() :]
    if end_match:
        text = text[: end_match.start()]

    return text.strip()


def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    return text


def chunk_text(text, min_length=150, max_length=500):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    sentence_end = re.compile(r"(?<=[.!?])\s+")

    chunks = []
    buffer = ""
    for p in paragraphs:
        sentences = sentence_end.split(p)
        for s in sentences:
            if len(buffer) + len(s) > max_length and len(buffer) >= min_length:
                chunks.append(buffer.strip())
                buffer = ""
            buffer += " " + s
    if buffer.strip():
        chunks.append(buffer.strip())

    return chunks


def embed_in_batches(client, chunks, batch_size=50):
    all_embeddings = []
    total = len(chunks)
    for i in range(0, total, batch_size):
        batch = chunks[i : i + batch_size]
        response = client.generate_embeddings(batch)
        all_embeddings.extend([item.embedding for item in response.data])
        print(f"\r{min(i + batch_size, total)}/{total} processed", end="", flush=True)
    print()
    return all_embeddings


def load_all_chunks():
    all_chunks = []

    for filepath in glob.glob(os.path.join(DATA_DIR, "*.txt")):
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        cleaned = clean_gutenberg_text(raw)
        chunks = chunk_text(cleaned)
        all_chunks.extend(chunks)
        print(f"{os.path.basename(filepath)}: {len(chunks)} chunks generated.")

    for filepath in glob.glob(os.path.join(DATA_DIR, "*.pdf")):
        raw = extract_text_from_pdf(filepath)
        cleaned = clean_pdf_text(raw)
        chunks = chunk_text(cleaned)
        all_chunks.extend(chunks)
        print(f"{os.path.basename(filepath)}: {len(chunks)} chunks generated.")

    return all_chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing database and re-ingest",
    )
    args = parser.parse_args()

    config = Configuration(app_name="foundry_local_samples")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance
    manager.download_and_register_eps(progress_callback=lambda ep, pct: None)

    model = manager.catalog.get_model("qwen3-embedding-0.6b")
    model.download(lambda p: print(f"\rDownloading: {p:.1f}%", end="", flush=True))
    print()
    model.load()
    print("Embedding model loaded.")

    client = model.get_embedding_client()

    init_db()

    if args.reset:
        clear_documents()
        print("Database cleared.")

    existing = get_all_documents()
    if existing:
        print(
            f"Found {len(existing)} chunks already in the database, skipping ingestion."
        )
    else:
        chunks = load_all_chunks()
        print(f"Embedding a total of {len(chunks)} chunks...")
        embeddings = embed_in_batches(client, chunks, batch_size=50)
        for chunk, embedding in zip(chunks, embeddings):
            insert_document(chunk, embedding)
        print("All chunks have been saved to the database.")

    model.unload()


if __name__ == "__main__":
    main()
