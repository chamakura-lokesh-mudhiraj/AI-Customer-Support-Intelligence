from fastapi import APIRouter

from app.models.ask import AskRequest
from app.models.rag_response import RAGResponse
from app.services.rag_service import answer_question


router = APIRouter(
    prefix="/ask",
    tags=["RAG"],
)


@router.post("/", response_model=RAGResponse)
def ask_question(request: AskRequest) -> RAGResponse:
    return answer_question(request.question)