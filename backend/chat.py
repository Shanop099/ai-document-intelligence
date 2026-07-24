from backend.embeddings import embedding_service
from backend.groq_client import groq_client
from backend.prompt_loader import PromptLoader
from backend.qdrant_service import qdrant_service


class ChatService:

    def ask(
        self,
        question: str,
        document_id: str
    ):

        # Generate query embedding
        query_embedding = embedding_service.generate_embedding(question)

        # Search only inside current document
        results = qdrant_service.search_document(
            query_embedding=query_embedding,
            document_id=document_id,
            limit=3
        )

        if not results:
            return "No relevant information found."

        context = ""

        for result in results:

            payload = result.payload

            context += f"""
Document Type:
{payload["document_type"]}

Document Content:
{payload["text"]}

----------------------------------
"""

        prompt = PromptLoader.load("qa.txt")

        prompt = prompt.replace(
            "{context}",
            context
        )

        prompt = prompt.replace(
            "{question}",
            question
        )

        answer = groq_client.generate(prompt)

        return answer.strip()


chat_service = ChatService()