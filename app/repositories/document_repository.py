from app.db.models import Document, DocumentChunk


class DocumentRepository:

    def __init__(self, db):
        self.db = db

    # -----------------------------
    # CREATE DOCUMENT
    # -----------------------------
    def create_document(
        self,
        filename: str,
        file_type: str
    ):
        document = Document(
            filename=filename,
            file_type=file_type
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document
    
    
    def add_chunk(
        self,
        document_id: str,
        page: int,
        chunk_text: str,
        embedding
    ):
        chunk = DocumentChunk(
            document_id=str(document_id),
            page=page,
            chunk_text=chunk_text,
            embedding=embedding
        )

        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)

        return chunk
    # -----------------------------
    # GET DOCUMENT
    # -----------------------------
    def get_document(
        self,
        document_id: str
    ):
        document_id = str(document_id)

        return (
            self.db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

    # -----------------------------
    # GET ALL DOCUMENTS
    # -----------------------------
    def get_all_documents(self):

        return (
            self.db.query(Document)
            .order_by(
                Document.created_at.desc()
            )
            .all()
        )

    # -----------------------------
    # SEARCH CHUNKS
    # -----------------------------
    def search_chunks(
        self,
        query_embedding,
        document_id,
        limit=5
    ):

        document_id = str(document_id)

        return (
            self.db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
            .all()
        )

    # -----------------------------
    # DELETE DOCUMENT
    # -----------------------------
    def delete_document(
        self,
        document_id: str
    ) -> bool:

        document_id = str(document_id)

        document = (
            self.db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if document is None:
            return False

        self.db.delete(document)
        self.db.commit()

        return True