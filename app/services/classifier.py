import json

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
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


def classify_ticket(ticket: Ticket) -> TicketClassification:
    prompt = f"""
Customer support ticket:

Subject:
{ticket.subject}

Message:
{ticket.message}
"""

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )

    result = json.loads(response.output_text)

    return TicketClassification.model_validate(result)