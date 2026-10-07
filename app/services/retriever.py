from app.services.embedding_service import create_embedding
from app.services.vector_store import VectorStore


def retrieve_relevant_chunks(
    question: str,
    vector_store: VectorStore | None = None,
    n_results: int = 3,
) -> dict:
    """Retrieve knowledge-base chunks relevant to a question."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if n_results <= 0:
        raise ValueError("n_results must be greater than zero.")

    if vector_store is None:
        vector_store = VectorStore()

    question_embedding = create_embedding(question)

    return vector_store.search(
        embedding=question_embedding,
        n_results=n_results,
    )