from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models.rag_response import RAGResponse


client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are a customer support assistant.

Answer the customer's question using only the provided
knowledge-base context.

Rules:
- Do not invent policies, prices, timelines, or procedures.
- If the context does not contain enough information,
  say that the available knowledge base does not provide
  enough information to answer the question.
- Give a concise and helpful customer-support answer.
"""


def generate_answer(
    question: str,
    context: str,
    sources: list[str],
) -> RAGResponse:
    """Generate a grounded answer from retrieved context."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not context.strip():
        raise ValueError("Context cannot be empty.")

    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions=SYSTEM_PROMPT,
        input=f"""
Customer question:

{question}

Knowledge-base context:

{context}
""",
    )

    return RAGResponse(
        answer=response.output_text.strip(),
        sources=sources,
    )