from app.services.embedding_service import create_embedding
from app.services.vector_store import VectorStore


MAX_DISTANCE = 1.5
MAX_DISTANCE_RATIO = 1.25


def retrieve_relevant_chunks(
    question: str,
    vector_store: VectorStore | None = None,
    n_results: int = 3,
) -> dict:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if n_results <= 0:
        raise ValueError("n_results must be greater than zero.")

    if vector_store is None:
        vector_store = VectorStore()

    question_embedding = create_embedding(question)

    results = vector_store.search(
        embedding=question_embedding,
        n_results=n_results,
    )

    distances = results.get("distances", [[]])[0]

    if not distances:
        return results

    best_distance = min(distances)

    max_allowed_distance = (
        best_distance * MAX_DISTANCE_RATIO
    )

    relevant_indexes = [
        index
        for index, distance in enumerate(distances)
        if (
            distance <= MAX_DISTANCE
            and distance <= max_allowed_distance
        )
    ]

    results["documents"] = [
        [
            document
            for index, document in enumerate(
                results.get("documents", [[]])[0]
            )
            if index in relevant_indexes
        ]
    ]

    results["metadatas"] = [
        [
            metadata
            for index, metadata in enumerate(
                results.get("metadatas", [[]])[0]
            )
            if index in relevant_indexes
        ]
    ]

    results["ids"] = [
        [
            item_id
            for index, item_id in enumerate(
                results.get("ids", [[]])[0]
            )
            if index in relevant_indexes
        ]
    ]

    results["distances"] = [
        [
            distance
            for index, distance in enumerate(distances)
            if index in relevant_indexes
        ]
    ]

    return results