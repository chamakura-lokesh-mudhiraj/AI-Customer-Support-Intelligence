from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class Ticket(BaseModel):
    ticket_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)

    subject: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)

    category: str | None = None
    priority: Literal["low", "medium", "high", "urgent"] | None = None
    sentiment: Literal["positive", "neutral", "negative"] | None = None

    status: Literal["open", "in_progress", "resolved", "closed"] = "open"

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )