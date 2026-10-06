from app.models.document import DocumentContent
from app.services.chunker import create_document_chunks


def test_create_document_chunks():
    document = DocumentContent(
        filename="refund_policy.docx",
        file_type="docx",
        text="A" * 1200,
        character_count=1200,
    )

    chunks = create_document_chunks(
        document,
        chunk_size=500,
        overlap=50,
    )

    assert len(chunks) == 3

    assert chunks[0].chunk_id == 0
    assert chunks[1].chunk_id == 1
    assert chunks[2].chunk_id == 2

    assert chunks[0].filename == "refund_policy.docx"

    assert len(chunks[0].text) == 500
    assert len(chunks[1].text) == 500
    assert len(chunks[2].text) == 300


def test_create_document_chunks_empty_document():
    document = DocumentContent(
        filename="empty.docx",
        file_type="docx",
        text="",
        character_count=0,
    )

    chunks = create_document_chunks(document)

    assert chunks == []