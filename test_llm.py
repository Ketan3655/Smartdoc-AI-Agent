from app.services.llm_service import LLMService


llm = LLMService()


answer = llm.generate_answer(
    question="What is SmartDoc AI?",
    context="""
SmartDoc AI is a document intelligence application.
It allows users to upload documents and ask questions
about their contents.
"""
)


print(answer)