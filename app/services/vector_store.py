import chromadb

from app.models.document_chunk import DocumentChunk


class VectorStore:
    def __init__(self, collection_name: str = "support_knowledge"):
        self.client = chromadb.PersistentClient(
            path="./data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must match the number of embeddings."
            )

        if not chunks:
            return

        self.collection.add(
            ids=[
                f"{chunk.filename}-{chunk.chunk_id}"
                for chunk in chunks
            ],
            documents=[
                chunk.text
                for chunk in chunks
            ],
            embeddings=embeddings,
            metadatas=[
                {
                    "filename": chunk.filename,
                    "chunk_id": chunk.chunk_id,
                }
                for chunk in chunks
            ],
        )

    def search(
        self,
        embedding: list[float],
        n_results: int = 3,
    ) -> dict:
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )