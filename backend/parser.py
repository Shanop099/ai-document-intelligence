from pathlib import Path
import fitz


class DocumentParser:

    @staticmethod
    def extract_pdf_text(pdf_path: str):
        """
        Extract text from a PDF.
        Returns the extracted text and whether it is scanned.
        """

        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        is_scanned = len(text.strip()) < 50

        return text, is_scanned

    @staticmethod
    def get_extension(file_path: str):
        return Path(file_path).suffix.lower()