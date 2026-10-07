from app.models.document_chunk import DocumentChunk
from app.models.rag_response import RAGResponse
from app.services.rag_service import answer_question
from app.services.vector_store import VectorStore


def test_answer_question(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    vector_store = VectorStore(
        collection_name="test_rag"
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

    monkeypatch.setattr(
        "app.services.rag_service.retrieve_relevant_chunks",
        lambda question, vector_store, n_results: {
            "documents": [
                [
                    "Customers can request a refund within thirty days."
                ]
            ],
            "metadatas": [
                [
                    {
                        "filename": "refund_policy.txt",
                        "chunk_id": 0,
                    }
                ]
            ],
        },
    )

    monkeypatch.setattr(
        "app.services.rag_service.generate_answer",
        lambda question, context, sources: RAGResponse(
            answer="You can request a refund within thirty days.",
            sources=sources,
        ),
    )

    result = answer_question(
        question="How long do I have to request a refund?",
        vector_store=vector_store,
        n_results=1,
    )

    assert result.answer == (
        "You can request a refund within thirty days."
    )

    assert result.sources == ["refund_policy.txt"]

def test_answer_question_returns_only_relevant_sources(monkeypatch):
    monkeypatch.setattr(
        "app.services.rag_service.retrieve_relevant_chunks",
        lambda question, vector_store, n_results: {
            "documents": [
                [
                    "If your account is compromised, change your password immediately.",
                    "Use the password reset option on the sign-in page.",
                ]
            ],
            "metadatas": [
                [
                    {
                        "filename": "account_security.txt",
                        "chunk_id": 0,
                    },
                    {
                        "filename": "password_reset.txt",
                        "chunk_id": 0,
                    },
                ]
            ],
        },
    )

    monkeypatch.setattr(
        "app.services.rag_service.generate_answer",
        lambda question, context, sources: RAGResponse(
            answer=(
                "Change your password immediately and "
                "contact customer support."
            ),
            sources=sources,
        ),
    )

    result = answer_question(
        question="I think someone accessed my account.",
        vector_store=None,
        n_results=3,
    )

    assert result.answer == (
        "Change your password immediately and "
        "contact customer support."
    )

    assert result.sources == [
        "account_security.txt",
        "password_reset.txt",
    ]