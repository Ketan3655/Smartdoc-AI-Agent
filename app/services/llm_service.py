import os
import httpx


class LLMService:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY is missing. Add it to your .env file."
            )

        self.client = httpx.Client(
            base_url="https://api.groq.com/openai/v1",
            timeout=60.0
        )

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = f"""
You are a helpful document question-answering assistant.

Answer ONLY using the document context.

If the answer is not in the context, say:

"I could not find the answer in the uploaded document."

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}
"""

        messages = [
            {
                "role": "system",
                "content":
                "You answer only from the provided document."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self._call_llm(messages)

    def chat(
        self,
        message: str,
        context: str,
        history: list
    ) -> str:

        messages = [
            {
                "role": "system",
                "content":
                "You are a helpful AI assistant. Answer ONLY using the provided document context."
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content":
                f"""
DOCUMENT CONTEXT:

{context}

QUESTION:

{message}
"""
            }
        )

        return self._call_llm(messages)

    def _call_llm(self, messages):

        response = self.client.post(
            "/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 800
            }
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]