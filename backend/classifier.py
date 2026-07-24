from pathlib import Path

from backend.groq_client import groq_client


class DocumentClassifier:

    SUPPORTED_TYPES = {
        "PAN Card",
        "Aadhaar Card",
        "GST Certificate",
        "FSSAI License",
        "Driving License",
        "Passport",
        "Unknown",
    }

    def __init__(self):
        prompt_path = Path("prompts/classify.txt")
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

    def classify(self, document: dict) -> dict:

        text = document.get("text", "").strip()

        if not text:
            document["document_type"] = "Unknown"
            return document

        prompt = self.prompt_template.replace("{text}", text)

        response = groq_client.generate(prompt).strip()

        if response not in self.SUPPORTED_TYPES:
            response = "Unknown"

        document["document_type"] = response

        return document