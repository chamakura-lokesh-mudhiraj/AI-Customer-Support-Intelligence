from app.models.ticket import Ticket
from app.models.classification import TicketClassification
from app.services import classifier


def test_classify_ticket(monkeypatch):
    ticket = Ticket(
        ticket_id="TICKET-001",
        customer_id="CUSTOMER-001",
        subject="Unable to login",
        message="I cannot access my account.",
    )

    class FakeResponse:
        output_text = """
        {
            "category": "authentication",
            "priority": "high",
            "sentiment": "negative"
        }
        """

    def fake_create(**kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        classifier.client.responses,
        "create",
        fake_create,
    )

    result = classifier.classify_ticket(ticket)

    assert isinstance(result, TicketClassification)
    assert result.category == "authentication"
    assert result.priority == "high"
    assert result.sentiment == "negative"