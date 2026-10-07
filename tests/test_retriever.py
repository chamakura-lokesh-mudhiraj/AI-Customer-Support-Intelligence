from app.models.document_chunk import DocumentChunk
from app.services.retriever import retrieve_relevant_chunks
from app.services.vector_store import VectorStore


def test_retrieve_relevant_chunks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    vector_store = VectorStore(
        collection_name="test_retrieval"
    )

    chunks = [
        DocumentChunk(
            chunk_id=0,
            filename="refund_policy.txt",
            text="Customers can request a refund within thirty days.",
        ),
        DocumentChunk(
            chunk_id=1,
            filename="shipping_policy.txt",
            text="Orders usually ship within three business days.",
        ),
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]

    vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    def fake_create_embedding(question: str) -> list[float]:
        assert "refund" in question.lower()
        return [1.0, 0.0, 0.0]

    monkeypatch.setattr(
        "app.services.retriever.create_embedding",
        fake_create_embedding,
    )

    results = retrieve_relevant_chunks(
        "How long do I have to request a refund?",
        vector_store=vector_store,
        n_results=1,
    )

    assert len(results["documents"]) == 1

    assert results["documents"][0][0] == (
        "Customers can request a refund within thirty days."
    )

    assert results["metadatas"][0][0]["filename"] == (
        "refund_policy.txt"
    )


def test_retrieve_rejects_empty_question():
    try:
        retrieve_relevant_chunks("")
        assert False
    except ValueError as exc:
        assert "Question cannot be empty." in str(exc)