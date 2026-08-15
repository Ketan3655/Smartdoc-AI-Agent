from app.db.models import ChatSession, ChatMessage


class ChatRepository:

    def __init__(self, db):
        self.db = db

    def create_session(self, document_id: str):
        session = ChatSession(
            document_id=str(document_id)
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_session(self, session_id: str):
        return (
            self.db.query(ChatSession)
            .filter(
                ChatSession.id == str(session_id)
            )
            .first()
        )

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):
        message = ChatMessage(
            session_id=str(session_id),
            role=role,
            content=content
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_messages(self, session_id: str):
        return (
            self.db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == str(session_id)
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
            .all()
        )