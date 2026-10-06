from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.ticket import Ticket
from app.models.ticket_db import TicketDB
from app.services.classifier import classify_ticket
from app.services.ticket_repository import create_ticket


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket_endpoint(
    ticket: Ticket,
    db: Session = Depends(get_db),
) -> Ticket:

    analysis = classify_ticket(ticket)

    ticket.category = analysis.classification.category
    ticket.priority = analysis.classification.priority
    ticket.sentiment = analysis.classification.sentiment

    db_ticket = TicketDB(
        ticket_id=ticket.ticket_id,
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        message=ticket.message,
        category=ticket.category,
        priority=ticket.priority,
        sentiment=ticket.sentiment,
        status=ticket.status,
        created_at=ticket.created_at,
    )

    create_ticket(db, db_ticket)

    return ticket