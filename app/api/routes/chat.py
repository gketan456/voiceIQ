from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.support_agent import process_message
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
    tools_used: list

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    logger.info(f"Message received session={request.session_id}")
    
    result = await process_message(
        message=request.message,
        session_id=request.session_id,
        customer_id=request.customer_id,
    )
    
    return ChatResponse(
        response=result["response"],
        session_id=result["session_id"],
        tools_used=result["tools_used"],
    )
