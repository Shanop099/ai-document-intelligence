from backend.parser import DocumentParser

pdf = "uploads/IshanResume.pdf"

print("Extension:")
print(DocumentParser.get_extension(pdf))

print()

print("Scanned?")
print(DocumentParser.is_scanned_pdf(pdf))

print()

print("Extracted Text")
print(DocumentParser.extract_pdf_text(pdf))