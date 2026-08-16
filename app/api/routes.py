import uuid

# from app.schemas.chat import (
#     AskDocumentRequest,
#     AskDocumentResponse,
#     DocumentListResponse
# )
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
     ChatHistoryResponse,
    ChatMessage,
    SourceResponse
)

from app.services.chat_service import ChatService
from app.repositories.document_repository import DocumentRepository
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from pathlib import Path
from app.services.agent import SmartDocAgent
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.repositories.chat_repository import ChatRepository
from app.db.database import get_db
from app.services.document_service import DocumentService
from app.services.search_service import SearchService
from app.api.auth_dependencies import get_current_user
from app.db.models import User
router = APIRouter(prefix="/documents", tags=["Documents"])


ALLOWED_TYPES = {".pdf", ".docx", ".txt"}

current_user: User = Depends(get_current_user)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
    
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are supported"
        )
    # Create uploads folder
    upload_dir = Path("uploads")

    upload_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = upload_dir / unique_filename

    # Save uploaded file
    content = await file.read()

    with open(file_path, "wb") as saved_file:

        saved_file.write(content)

    try:
        document_service = DocumentService(db)

        result = document_service.upload_document(
            file_path=file_path, filename=file.filename, file_type=extension
        )

        return {
            "message": ("Document uploaded and " "processed successfully"),
            "document_id": (result["document_id"]),
            "filename": file.filename,
            "total_chunks": (result["chunks"]),
        }

    except Exception as error:

        raise HTTPException(status_code=500, detail=str(error))

@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    session: Session = Depends(get_db),  
    current_user: User = Depends(get_current_user)
    
):
    print("\n========== CHAT DEBUG ==========")
    print("DOCUMENT ID:", repr(request.document_id))
    print("MESSAGE:", repr(request.message))
    print("SESSION ID:", repr(request.session_id))

    try:
        print("STEP 1: Creating ChatService")

        service = ChatService(session)

        print("STEP 2: Calling ChatService.chat()")

        result = service.chat(
            document_id=request.document_id,
            message=request.message,
            session_id=request.session_id
        )

        print("STEP 3: ChatService completed")
        print("RESULT:", result)
        print("========== CHAT SUCCESS ==========\n")

        return result

    except Exception as error:

        print("\n========== CHAT ERROR ==========")
        print("ERROR TYPE:", type(error))
        print("ERROR:", repr(error))

        import traceback
        traceback.print_exc()

        print("========== END CHAT ERROR ==========\n")

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
        
@router.get(
    "/chat/{session_id}",
    response_model=ChatHistoryResponse
)
def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):
    repository = ChatRepository(db)

    session = repository.get_session(
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    messages = repository.get_messages(
        session_id
    )

    return {
        "session_id": str(session.id),
        "document_id": str(session.document_id),
        "messages": [
            {
                "role": message.role,
                "content": message.content
            }
            for message in messages
        ]
    }
@router.get("/search")
def search_documents(
    query: str,
    document_id: str | None = None,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not query.strip():

        raise HTTPException(status_code=400, detail=("Query cannot be empty"))

    if limit < 1 or limit > 20:

        raise HTTPException(
            status_code=400, detail=("Limit must be between " "1 and 20")
        )

    search_service = SearchService(db)

    results = search_service.search(query=query, document_id=document_id, limit=limit)

    return {"query": query, "total_results": len(results), "results": results}




@router.post("/ask", response_model=ChatResponse)
def ask_document(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    agent = SmartDocAgent(db=db)

    result = agent.ask(
        question=request.question, document_id=request.document_id, limit=request.limit
    )

    return result


@router.get(
    "/",
)
def list_documents(db: Session = Depends(get_db)):

    repository = DocumentRepository(db=db)

    documents = repository.get_all_documents()
    current_user: User = Depends(get_current_user)

    return {"documents": documents}


@router.delete("/{document_id}")
def delete_document(document_id: str, session: Session = Depends(get_db)):
    from app.db.models import Document

    print("DELETE REQUEST ID:", repr(document_id))

    documents = session.query(Document).all()

    print("DATABASE DOCUMENT IDs:")
    for document in documents:
        print("ID:", repr(document.id), "TYPE:", type(document.id))

    document = session.query(Document).filter(Document.id == str(document_id)).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Document not found",
                "requested_id": document_id,
                "available_ids": [str(item.id) for item in documents],
            },
        )

    session.delete(document)
    session.commit()

    return {"message": "Document deleted successfully", "document_id": str(document_id)}
