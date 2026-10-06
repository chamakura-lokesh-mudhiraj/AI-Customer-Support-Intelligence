from fastapi.testclient import TestClient

from app.api import tickets
from app.main import app
from app.models.analysis import TicketAnalysis
from app.models.classification import TicketClassification


client = TestClient(app)


def test_create_ticket(monkeypatch):
    def fake_classify_ticket(ticket):
        return TicketAnalysis(
            classification=TicketClassification(
                category="authentication",
                priority="high",
                sentiment="negative",
            ),
            model="test-model",
            processing_time_ms=12.5,
        )

    monkeypatch.setattr(
        tickets,
        "classify_ticket",
        fake_classify_ticket,
    )

    response = client.post(
        "/tickets/",
        json={
            "ticket_id": "TICKET-001",
            "customer_id": "CUSTOMER-001",
            "subject": "Unable to login",
            "message": "I cannot access my account.",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["category"] == "authentication"
    assert data["priority"] == "high"
    assert data["sentiment"] == "negative"