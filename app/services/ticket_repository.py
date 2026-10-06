from sqlalchemy.orm import Session

from app.models.ticket_db import TicketDB


def create_ticket(db: Session, ticket: TicketDB) -> TicketDB:
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket