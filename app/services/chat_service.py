from app.services.search_service import SearchService
from app.services.llm_service import LLMService
from app.repositories.chat_repository import ChatRepository


class ChatService:

    def __init__(self, db):
        self.search_service = SearchService(db)
        self.chat_repository = ChatRepository(db)
        self.llm_service = LLMService()

    def chat(
        self,
        document_id: str,
        message: str,
        session_id: str | None = None,
        limit: int = 5,
    ):

        # --------------------------------------------------
        # 1. Verify / create chat session
        # --------------------------------------------------

        if session_id:
            session = self.chat_repository.get_session(session_id)

            if session is None:
                session = self.chat_repository.create_session(document_id)
        else:
            session = self.chat_repository.create_session(document_id)

        # --------------------------------------------------
        # 2. Get previous messages
        # --------------------------------------------------

        previous_messages = self.chat_repository.get_messages(str(session.id))

        history = [
            {"role": message.role, "content": message.content}
            for message in previous_messages
        ]

        # --------------------------------------------------
        # 3. Search document
        # --------------------------------------------------

        chunks = self.search_service.search(
            query=message, document_id=document_id, limit=limit
        )

        context = "\n\n".join(
            chunk.get("chunk_text") or chunk.get("text", "") for chunk in chunks
        )

        # --------------------------------------------------
        # 4. Generate answer
        # --------------------------------------------------

        answer = self.llm_service.chat(
            message=message, context=context, history=history
        )

        # --------------------------------------------------
        # 5. Save user message
        # --------------------------------------------------

        self.chat_repository.add_message(
            session_id=str(session.id), role="user", content=message
        )

        # --------------------------------------------------
        # 6. Save assistant message
        # --------------------------------------------------

        self.chat_repository.add_message(
            session_id=str(session.id), role="assistant", content=answer
        )

        # --------------------------------------------------
        # 7. Return
        # --------------------------------------------------
        sources = [
    {
        "page": chunk.get("page"),
        "text": (
            chunk.get("chunk_text")
            or chunk.get("text", "")
        ),
    }
    for chunk in chunks
]


        return {"session_id": str(session.id), "answer": answer, "sources": sources}
