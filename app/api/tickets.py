from fastapi import APIRouter, status

from app.models.ticket import Ticket


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: Ticket) -> Ticket:
    return ticket