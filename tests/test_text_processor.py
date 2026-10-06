from app.services.text_processor import clean_text, chunk_text


def test_clean_text():
    text = "  Hello    world.\r\n\r\n\r\nThis is   a test.  "

    cleaned = clean_text(text)

    assert cleaned == "Hello world.\n\nThis is a test."


def test_chunk_text():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = chunk_text(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert len(chunks) == 3
    assert chunks[0] == "abcdefghij"
    assert chunks[1] == "ijklmnopqr"
    assert chunks[2] == "qrstuvwxyz"


def test_chunk_text_empty():
    assert chunk_text("") == []


def test_chunk_text_invalid_overlap():
    try:
        chunk_text("some text", chunk_size=10, overlap=10)
        assert False
    except ValueError as exc:
        assert "overlap must be smaller" in str(exc)