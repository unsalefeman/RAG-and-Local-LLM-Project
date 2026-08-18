from foundry_local_sdk import Configuration, FoundryLocalManager
from retrieval import get_top_chunks, init_embedding_client


_chat_model = None
_chat_client = None


def init_chat_client():
    global _chat_model, _chat_client

    manager = (
        FoundryLocalManager.instance
    )  # already initialized, do not re-initialize

    _chat_model = manager.catalog.get_model("phi-3.5-mini")
    _chat_model.download(lambda p: None)
    _chat_model.load()
    _chat_client = _chat_model.get_chat_client()


def build_prompt(question, chunks):
    context = "\n\n---\n\n".join(chunk for _, chunk in chunks)

    system_message = (
        "You are a helpful assistant that answers questions using ONLY the "
        "provided context below. Do not use any outside knowledge, even if "
        "you know the answer. If the context does not contain enough "
        "information to answer the question, say so explicitly instead of "
        "guessing or adding information from elsewhere. Keep answers concise "
        "and directly grounded in the given text."
    )

    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]


def answer_query(question, k=3):
    chunks = get_top_chunks(question, k=k)
    messages = build_prompt(question, chunks)

    print("Answer: ", end="", flush=True)
    full_response = ""
    for chunk in _chat_client.complete_streaming_chat(messages):
        if chunk.choices and chunk.choices[0].delta.content:
            piece = chunk.choices[0].delta.content
            print(piece, end="", flush=True)
            full_response += piece
    print()
    return full_response


def main():
    print("Preparing embedding model...")
    init_embedding_client()

    print("Preparing chat model...")
    init_chat_client()

    print("\nReady! Ask your questions (type 'q' to quit).\n")

    while True:
        question = input("Question: ").strip()
        if question.lower() in ("q", "quit", "exit"):
            break
        if not question:
            continue
        answer_query(question)
        print()


if __name__ == "__main__":
    main()
