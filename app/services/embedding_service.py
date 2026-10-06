from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def create_embedding(text: str) -> list[float]:
    """Create an embedding for a single piece of text."""
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
        encoding_format="float",
    )

    return response.data[0].embedding