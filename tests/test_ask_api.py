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

def test_ask_question_with_no_relevant_knowledge(monkeypatch):
    def fake_answer_question(question):
        assert question == "What is the weather today?"

        return RAGResponse(
            answer=(
                "The available knowledge base does not contain "
                "enough information to answer this question."
            ),
            sources=[],
        )

    monkeypatch.setattr(
        ask,
        "answer_question",
        fake_answer_question,
    )

    response = client.post(
        "/ask/",
        json={
            "question": "What is the weather today?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "The available knowledge base does not contain "
        "enough information to answer this question."
    )

    assert data["sources"] == []


def test_ask_question_with_multiple_sources(monkeypatch):
    def fake_answer_question(question):
        assert question == (
            "I think someone accessed my account."
        )

        return RAGResponse(
            answer=(
                "Change your password immediately and "
                "contact customer support."
            ),
            sources=[
                "account_security.txt",
                "password_reset.txt",
            ],
        )

    monkeypatch.setattr(
        ask,
        "answer_question",
        fake_answer_question,
    )

    response = client.post(
        "/ask/",
        json={
            "question": (
                "I think someone accessed my account."
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "Change your password immediately and "
        "contact customer support."
    )

    assert data["sources"] == [
        "account_security.txt",
        "password_reset.txt",
    ]