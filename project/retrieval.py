import numpy as np
from database import get_all_documents
from foundry_local_sdk import Configuration, FoundryLocalManager


_manager = None
_model = None
_client = None


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def init_embedding_client():
    global _manager, _model, _client

    config = Configuration(app_name="foundry_local_samples")
    FoundryLocalManager.initialize(config)
    _manager = FoundryLocalManager.instance
    _manager.download_and_register_eps(progress_callback=lambda ep, pct: None)

    _model = _manager.catalog.get_model("qwen3-embedding-0.6b")
    _model.download(lambda p: None)  # already downloaded, silently verifies
    _model.load()
    _client = _model.get_embedding_client()


def get_top_chunks(query, k=3):
    if _client is None:
        raise RuntimeError("init_embedding_client() must be called first.")

    query_response = _client.generate_embedding(query)
    query_embedding = query_response.data[0].embedding

    stored_docs = get_all_documents()
    scored = []
    for doc_id, content, embedding in stored_docs:
        score = cosine_similarity(query_embedding, embedding)
        scored.append((score, content))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:k]


if __name__ == "__main__":
    init_embedding_client()

    query = "Can you explain what is a derivative?"
    results = get_top_chunks(query, k=3)

    print(f"\nQuestion: {query}\n")
    for i, (score, content) in enumerate(results):
        print(f"{i+1}. (score: {score:.4f})")
        print(f"   {content[:150]}...")
        print()
