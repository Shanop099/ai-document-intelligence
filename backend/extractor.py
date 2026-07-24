import json

from backend.groq_client import groq_client
from backend.prompt_loader import PromptLoader


class DocumentExtractor:
    """
    Extracts structured information from a document
    using the detected document type and OCR text.
    """

    def extract(self, document: dict):

        prompt = PromptLoader.load("extract.txt")

        prompt = prompt.replace(
            "{document_type}",
            document["document_type"]
        )

        prompt = prompt.replace(
            "{text}",
            document["text"]
        )

        response = groq_client.generate(prompt).strip()

        # Remove markdown code fences if present
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        # Extract only the JSON object
        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:
            response = response[start:end + 1]

        try:
            document["extracted_data"] = json.loads(response)

        except json.JSONDecodeError:

            document["extracted_data"] = {
                "raw_response": response
            }

        return document