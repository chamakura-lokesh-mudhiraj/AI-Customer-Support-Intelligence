from typing import Literal

from pydantic import BaseModel


class TicketClassification(BaseModel):
    category: Literal[
        "authentication",
        "billing",
        "technical",
        "shipping",
        "account",
        "refund",
        "other",
    ]

    priority: Literal[
        "low",
        "medium",
        "high",
        "urgent",
    ]

    sentiment: Literal[
        "positive",
        "neutral",
        "negative",
    ]