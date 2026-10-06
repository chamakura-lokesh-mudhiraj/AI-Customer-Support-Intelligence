from pydantic import BaseModel

from app.models.classification import TicketClassification


class TicketAnalysis(BaseModel):
    classification: TicketClassification
    model: str
    processing_time_ms: float