from pydantic import BaseModel


class DocumentContent(BaseModel):
    filename: str
    file_type: str
    text: str
    character_count: int