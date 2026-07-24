from backend.ocr import OCRService

document = {
    "filename": "sample_pan.jpg",
    "filepath": "uploads/sample_pan.jpg",
    "extension": ".jpg",
    "text": "",
    "is_scanned": True
}

ocr = OCRService()

document = ocr.extract(document)

print(document["text"])