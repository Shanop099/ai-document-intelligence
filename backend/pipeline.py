import json
import uuid
from datetime import datetime
from pathlib import Path

from backend.parser import DocumentParser
from backend.ocr import OCRService
from backend.classifier import DocumentClassifier
from backend.extractor import DocumentExtractor
from backend.validator import DocumentValidator
from backend.embeddings import embedding_service


class DocumentPipeline:

    def __init__(self):
        self.ocr = OCRService()
        self.classifier = DocumentClassifier()
        self.extractor = DocumentExtractor()
        self.validator = DocumentValidator()

    def process(self, file_path: str):

        file_path = Path(file_path)

        document = {
            "document_id": str(uuid.uuid4()),

            "filename": file_path.name,
            "filepath": str(file_path),
            "extension": file_path.suffix.lower(),

            "text": "",
            "is_scanned": False,

            "document_type": None,
            "extracted_data": {},
            "validation": {},

            "embedding_text": "",
            "embedding": None,

            "json_path": None,

            "processed_at": datetime.now().isoformat()
        }

        # -----------------------------------------
        # Parse Document
        # -----------------------------------------

        if document["extension"] == ".pdf":

            text, scanned = DocumentParser.extract_pdf_text(str(file_path))

            document["text"] = text
            document["is_scanned"] = scanned

        else:
            # Images always require OCR
            document["is_scanned"] = True

        # -----------------------------------------
        # OCR
        # -----------------------------------------

        document = self.ocr.extract(document)

        # -----------------------------------------
        # Document Classification
        # -----------------------------------------

        document = self.classifier.classify(document)

        # -----------------------------------------
        # Information Extraction
        # -----------------------------------------

        document = self.extractor.extract(document)

        # -----------------------------------------
        # Validation
        # -----------------------------------------

        document = self.validator.validate(document)

        # -----------------------------------------
        # Build Structured Embedding Text
        # -----------------------------------------

        document["embedding_text"] = f"""
Document ID:
{document["document_id"]}

Document Type:
{document["document_type"]}

Extracted Data:
{json.dumps(document["extracted_data"], indent=2, ensure_ascii=False)}

Validation:
{json.dumps(document["validation"], indent=2, ensure_ascii=False)}

OCR Text:
{document["text"]}
""".strip()

        # -----------------------------------------
        # Generate Embedding
        # -----------------------------------------

        document["embedding"] = embedding_service.generate_embedding(
            document["embedding_text"]
        )

        # -----------------------------------------
        # Save JSON
        # -----------------------------------------

        output_dir = Path("extracted_json")
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        json_path = output_dir / f"{file_path.stem}_{timestamp}.json"

        json_document = {
            "document_id": document["document_id"],
            "filename": document["filename"],
            "filepath": document["filepath"],
            "document_type": document["document_type"],

            "extracted_data": document["extracted_data"],

            "validation": document["validation"],

            "ocr_text": document["text"],

            "embedding_text": document["embedding_text"],

            "processed_at": document["processed_at"]
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(
                json_document,
                f,
                indent=4,
                ensure_ascii=False
            )

        document["json_path"] = str(json_path)

        return document