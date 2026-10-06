from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models.ticket_db import TicketDB
from app.services.ticket_repository import create_ticket


def test_create_ticket():
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

    db = TestingSessionLocal()

    ticket = TicketDB(
        ticket_id="TICKET-DB-001",
        customer_id="CUSTOMER-001",
        subject="Payment failed",
        message="My payment was declined.",
        category="billing",
        priority="high",
        sentiment="negative",
        status="open",
    )

    result = create_ticket(db, ticket)

    assert result.ticket_id == "TICKET-DB-001"
    assert result.category == "billing"
    assert result.priority == "high"

    saved_ticket = db.get(TicketDB, "TICKET-DB-001")

    assert saved_ticket is not None
    assert saved_ticket.message == "My payment was declined."

    db.close()