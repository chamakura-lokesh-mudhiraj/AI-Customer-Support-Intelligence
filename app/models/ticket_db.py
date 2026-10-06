from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TicketDB(Base):
    __tablename__ = "tickets"

    ticket_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    customer_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    category: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    priority: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    sentiment: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String,
        default="open",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )