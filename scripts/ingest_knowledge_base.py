import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.knowledge_base import ingest_document


DOCUMENTS_DIR = PROJECT_ROOT / "documents"


def main() -> None:
    documents = sorted(DOCUMENTS_DIR.glob("*.txt"))

    if not documents:
        print("No .txt documents found.")
        return

    for document_path in documents:
        chunks = ingest_document(str(document_path))

        print(
            f"{document_path.name}: "
            f"{len(chunks)} chunk(s) ingested"
        )


if __name__ == "__main__":
    main()