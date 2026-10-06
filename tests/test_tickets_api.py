from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import tickets
from app.core.database import Base, get_db
from app.main import app
from app.models.analysis import TicketAnalysis
from app.models.classification import TicketClassification


engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

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
            "ticket_id": "TICKET-API-001",
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