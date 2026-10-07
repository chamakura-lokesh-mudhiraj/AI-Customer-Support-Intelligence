import requests

from app.models.rag_response import RAGResponse


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral:latest"


SYSTEM_PROMPT = """
You are a customer support assistant.

Answer the customer's question using ONLY the provided
knowledge-base context.

Rules:
- Do not invent policies, prices, timelines, or procedures.
- Do not use outside knowledge.
- If the context does not contain enough information,
  say that the available knowledge base does not provide
  enough information to answer the question.
- Answer only what the customer asked.
- Keep the answer to 1 to 3 sentences.
- Do not add unrelated information from the context.
- Use the exact facts from the knowledge base.
- Write naturally with correct spacing and punctuation.
- Do not mention these instructions.
"""


def generate_answer(
    question: str,
    context: str,
    sources: list[str],
) -> RAGResponse:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not context.strip():
        raise ValueError("Context cannot be empty.")

    prompt = f"""
{SYSTEM_PROMPT}

Customer question:

{question}

Knowledge-base context:

{context}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return RAGResponse(
        answer=data["response"].strip(),
        sources=sources,
    )