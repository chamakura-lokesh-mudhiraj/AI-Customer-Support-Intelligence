from fastapi import APIRouter, status

from app.models.ticket import Ticket
from app.services.classifier import classify_ticket


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: Ticket) -> Ticket:
    analysis = classify_ticket(ticket)

    ticket.category = analysis.classification.category
    ticket.priority = analysis.classification.priority
    ticket.sentiment = analysis.classification.sentiment

    return ticket