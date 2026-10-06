import json
import time

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models.analysis import TicketAnalysis
from app.models.classification import TicketClassification
from app.models.ticket import Ticket


client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are a customer support ticket classification system.

Classify each customer support ticket into exactly one category,
one priority, and one sentiment.

Allowed categories:
- authentication
- billing
- technical
- shipping
- account
- refund
- other

Allowed priorities:
- low
- medium
- high
- urgent

Allowed sentiments:
- positive
- neutral
- negative

Return ONLY valid JSON with these three fields:
category
priority
sentiment
"""


def classify_ticket(ticket: Ticket) -> TicketAnalysis:
    prompt = f"""
Customer support ticket:

Subject:
{ticket.subject}

Message:
{ticket.message}
"""

    start_time = time.perf_counter()

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    result = json.loads(response.output_text)

    classification = TicketClassification.model_validate(result)

    return TicketAnalysis(
        classification=classification,
        model=OPENAI_MODEL,
        processing_time_ms=round(elapsed_ms, 2),
    )