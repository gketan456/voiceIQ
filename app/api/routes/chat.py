from fastapi import APIRouter
from pydantic import BaseModel
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str
    customer_id: str = ""

class ChatResponse(BaseModel):
    response: str
    session_id: str

@router.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    logger.info(f"Message received session={request.session_id  }")
    return ChatResponse(
        response=f"You said: {request.message}",
        session_id=request.session_id,
    )   
