def build_context(results: dict) -> str:
    """Convert retrieval results into LLM-ready context."""

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return ""

    context_parts = []

    for document, metadata in zip(documents, metadatas):
        filename = metadata.get("filename", "unknown")
        chunk_id = metadata.get("chunk_id", "unknown")

        context_parts.append(
            f"[Source: {filename}, Chunk {chunk_id}]\n"
            f"{document}"
        )

    return "\n\n".join(context_parts)