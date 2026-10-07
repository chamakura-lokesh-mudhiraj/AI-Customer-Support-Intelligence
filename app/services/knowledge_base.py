from app.models.document_chunk import DocumentChunk
from app.services.chunker import create_document_chunks
from app.services.document_loader import load_document
from app.services.embedding_service import create_embedding
from app.services.vector_store import VectorStore


def ingest_document(
    file_path: str,
    vector_store: VectorStore | None = None,
) -> list[DocumentChunk]:
    """Load, chunk, embed, and store a document."""

    document = load_document(file_path)

    chunks = create_document_chunks(document)

    if not chunks:
        return []

    embeddings = [
        create_embedding(chunk.text)
        for chunk in chunks
    ]

    if vector_store is None:
        vector_store = VectorStore()

    vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    return chunks