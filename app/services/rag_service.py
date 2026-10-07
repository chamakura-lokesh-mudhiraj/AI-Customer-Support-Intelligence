from app.models.rag_response import RAGResponse
from app.services.answer_generator import generate_answer
from app.services.context_builder import build_context
from app.services.retriever import retrieve_relevant_chunks
from app.services.vector_store import VectorStore


def answer_question(
    question: str,
    vector_store: VectorStore | None = None,
    n_results: int = 3,
) -> RAGResponse:
    """Retrieve knowledge and generate a grounded answer."""

    results = retrieve_relevant_chunks(
        question=question,
        vector_store=vector_store,
        n_results=n_results,
    )

    context = build_context(results)

    if not context:
        return RAGResponse(
            answer=(
                "The available knowledge base does not contain "
                "enough information to answer this question."
            ),
            sources=[],
        )

    metadatas = results.get("metadatas", [[]])[0]

    sources = list(
        dict.fromkeys(
            metadata.get("filename", "unknown")
            for metadata in metadatas
        )
    )

    return generate_answer(
        question=question,
        context=context,
        sources=sources,
    )