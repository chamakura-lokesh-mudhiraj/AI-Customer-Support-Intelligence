from app.services.context_builder import build_context


def test_build_context():
    results = {
        "documents": [
            [
                "Customers can request a refund within thirty days.",
                "Refunds are processed within five business days.",
            ]
        ],
        "metadatas": [
            [
                {
                    "filename": "refund_policy.txt",
                    "chunk_id": 0,
                },
                {
                    "filename": "refund_policy.txt",
                    "chunk_id": 1,
                },
            ]
        ],
    }

    context = build_context(results)

    assert "[Source: refund_policy.txt, Chunk 0]" in context
    assert "Customers can request a refund" in context
    assert "[Source: refund_policy.txt, Chunk 1]" in context
    assert "Refunds are processed" in context


def test_build_context_empty():
    results = {
        "documents": [[]],
        "metadatas": [[]],
    }

    assert build_context(results) == ""