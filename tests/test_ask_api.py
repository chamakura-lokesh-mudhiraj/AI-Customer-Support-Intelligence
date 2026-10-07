from fastapi.testclient import TestClient

from app.main import app
from app.models.rag_response import RAGResponse
from app.api import ask


client = TestClient(app)


def test_ask_question(monkeypatch):
    def fake_answer_question(question):
        assert question == "How long do I have to request a refund?"

        return RAGResponse(
            answer="You can request a refund within thirty days.",
            sources=["refund_policy.txt"],
        )

    monkeypatch.setattr(
        ask,
        "answer_question",
        fake_answer_question,
    )

    response = client.post(
        "/ask/",
        json={
            "question": "How long do I have to request a refund?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "You can request a refund within thirty days."
    )

    assert data["sources"] == ["refund_policy.txt"]