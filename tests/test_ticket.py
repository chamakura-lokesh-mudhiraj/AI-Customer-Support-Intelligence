from app.models.ticket import Ticket


def test_ticket_creation():
    ticket = Ticket(
        ticket_id="TICKET-001",
        customer_id="CUSTOMER-001",
        subject="Unable to login",
        message="I have been unable to log into my account since this morning.",
    )

    assert ticket.ticket_id == "TICKET-001"
    assert ticket.customer_id == "CUSTOMER-001"
    assert ticket.status == "open"
    assert ticket.category is None
    assert ticket.priority is None
    assert ticket.sentiment is None