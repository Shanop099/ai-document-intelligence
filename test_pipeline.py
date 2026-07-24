from backend.pipeline import DocumentPipeline

pipeline = DocumentPipeline()

document = pipeline.process("uploads/sample_pan.jpg")

print("\n===== DOCUMENT PROCESSED =====\n")

print("Document Type:")
print(document["document_type"])

print("\nExtracted Data:")
print(document["extracted_data"])

print("\nValidation:")
print(document["validation"])

print("\nJSON Path:")
print(document["json_path"])