from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: int
    filename: str
    text: str