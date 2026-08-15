from typing import List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    document_id: str
    message: str
    history: List[ChatMessage] = []
    session_id: Optional[str] = None


class SourceResponse(BaseModel):
    page: Optional[int] = None
    text: str


class ChatResponse(BaseModel):
    answer: str | None=None
   
    sources: List[SourceResponse]
    session_id: str
    
class ChatHistoryMessage(BaseModel):
    role: str
    content: str


class ChatHistoryResponse(BaseModel):
    session_id: str
    document_id: str
    messages: list[ChatHistoryMessage]