from app.services.search_service import SearchService
from app.services.llm_service import LLMService


class SmartDocAgent:

    def __init__(self, db):
        self.search_service = SearchService(db=db)
        self.llm_service = LLMService()

    def ask(
        self,
        question: str,
        document_id: str,
        limit: int = 5
    ):

        search_results = self.search_service.search(
            query=question,
            document_id=document_id,
            limit=limit
        )

        if not search_results:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the uploaded document."
                ),
                "sources": []
            }

        context_parts = []
        sources = []

        for result in search_results:

            chunk_text = result.get(
                "text",
                result.get("chunk_text", "")
            )

            page = result.get(
                "page",
                None
            )

            context_parts.append(
                f"Page {page}:\n{chunk_text}"
            )

            sources.append(
                {
                    "page": page,
                    "text": chunk_text
                }
            )

        context = "\n\n---\n\n".join(context_parts)

        answer = self.llm_service.generate_answer(
            question=question,
            context=context
        )

        return {
            "answer": answer,
            "sources": sources
        }