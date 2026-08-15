from pathlib import Path
from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.services.parser import parse_document
from app.services.chunker import chunk_text
from app.services.embeddings import generate_embeddings


class DocumentService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = DocumentRepository(db)

    def upload_document(
        self,
        file_path: Path,
        filename: str,
        file_type: str
    ):

        # Parse
        pages = parse_document(file_path)

        # Chunk
        chunks = chunk_text(pages)

        # Embeddings
        embeddings = generate_embeddings(chunks)

        # Save document
        document = self.repository.create_document(
            filename=filename,
            file_type=file_type
        )

        # Save chunks
        for chunk, embedding in zip(chunks, embeddings):

            self.repository.add_chunk(
                document_id=document.id,
                page=chunk["page"],
                chunk_text=chunk["text"],
                embedding=embedding
            )

        return {
            "document_id": document.id,
            "chunks": len(chunks)
        }