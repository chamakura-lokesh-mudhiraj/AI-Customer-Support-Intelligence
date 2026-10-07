from pathlib import Path

from docx import Document
from pypdf import PdfReader

from app.models.document import DocumentContent


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages).strip()


def load_docx(file_path: str) -> str:
    document = Document(file_path)
    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()


def load_txt(file_path: str) -> str:
    path = Path(file_path)

    return path.read_text(
        encoding="utf-8",
    ).strip()


def load_document(file_path: str) -> DocumentContent:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        text = load_pdf(file_path)

    elif suffix == ".docx":
        text = load_docx(file_path)

    elif suffix == ".txt":
        text = load_txt(file_path)

    else:
        raise ValueError(
            f"Unsupported document type: {suffix}. "
            "Supported types are .pdf, .docx, and .txt."
        )

    return DocumentContent(
        filename=path.name,
        file_type=suffix.lstrip("."),
        text=text,
        character_count=len(text),
    )