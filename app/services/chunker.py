from app.models.document import DocumentContent
from app.models.document_chunk import DocumentChunk
from app.services.text_processor import chunk_text


def create_document_chunks(
    document: DocumentContent,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[DocumentChunk]:
    """Convert document text into structured chunks."""
    chunks = chunk_text(
        document.text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    return [
        DocumentChunk(
            chunk_id=index,
            filename=document.filename,
            text=text,
        )
        for index, text in enumerate(chunks)
    ]