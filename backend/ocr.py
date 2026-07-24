from pathlib import Path

from paddleocr import PaddleOCR
from PIL import Image
import fitz  # PyMuPDF


class OCRService:
    """
    Handles OCR for images and scanned PDFs.
    """

    def __init__(self):
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            lang="en"
        )

    def extract(self, document: dict) -> dict:
        """
        Performs OCR only if the document is scanned.
        Updates document["text"] and returns the document.
        """

        if not document["is_scanned"]:
            return document

        extension = document["extension"]

        if extension == ".pdf":
            text = self._extract_pdf(document["filepath"])
        else:
            text = self._extract_image(document["filepath"])

        document["text"] = text

        return document

    def _extract_image(self, image_path: str) -> str:

        result = self.ocr.predict(image_path)

        extracted_text = []

        for page in result:
            for line in page["rec_texts"]:
                extracted_text.append(line)

        return "\n".join(extracted_text)

    def _extract_pdf(self, pdf_path: str) -> str:

        doc = fitz.open(pdf_path)

        all_text = []

        for page in doc:

            pix = page.get_pixmap(dpi=300)

            temp_image = Path("temp_page.png")
            pix.save(temp_image)

            page_text = self._extract_image(str(temp_image))

            all_text.append(page_text)

            temp_image.unlink(missing_ok=True)

        doc.close()

        return "\n".join(all_text)