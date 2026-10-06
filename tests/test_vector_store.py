from app.models.document_chunk import DocumentChunk
from app.services.vector_store import VectorStore


def test_add_and_search_chunks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    store = VectorStore(
        collection_name="test_knowledge"
    )

    chunks = [
        DocumentChunk(
            chunk_id=0,
            filename="billing.txt",
            text="Customers can request a refund.",
        ),
        DocumentChunk(
            chunk_id=1,
            filename="shipping.txt",
            text="Orders usually ship within three days.",
        ),
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]

    store.add_chunks(chunks, embeddings)

    results = store.search(
        embedding=[1.0, 0.0, 0.0],
        n_results=1,
    )

    assert len(results["documents"]) == 1
    assert results["documents"][0][0] == (
        "Customers can request a refund."
    )

    assert results["metadatas"][0][0]["filename"] == "billing.txt"