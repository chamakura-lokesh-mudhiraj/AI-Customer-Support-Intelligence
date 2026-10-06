from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_ticket():
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

    assert data["ticket_id"] == "TICKET-001"
    assert data["customer_id"] == "CUSTOMER-001"
    assert data["status"] == "open"