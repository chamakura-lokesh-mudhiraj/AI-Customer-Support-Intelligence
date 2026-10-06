from app.models.analysis import TicketAnalysis
from app.models.ticket import Ticket
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

    assert isinstance(result, TicketAnalysis)
    assert result.classification.category == "authentication"
    assert result.classification.priority == "high"
    assert result.classification.sentiment == "negative"
    assert result.model
    assert result.processing_time_ms >= 0