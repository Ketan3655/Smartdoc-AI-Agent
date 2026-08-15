from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.services.embeddings import generate_embeddings


class SearchService:

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def search(
        self,
        query: str,
        document_id: int | None = None,
        limit: int = 5
    ):
        # Generate embedding for the user's question
        query_embedding = generate_embeddings(
            [query]
        )[0]

        # Search similar chunks
        chunks = self.repository.search_chunks(
            query_embedding=query_embedding,
            document_id=document_id,
            limit=limit
        )

        # Convert database objects into JSON
        results = []

        for chunk in chunks:
            results.append(
                {
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "page": chunk.page,
                    "text": chunk.chunk_text
                }
            )

        return results