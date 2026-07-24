from backend.validator import DocumentValidator

document = {
    "document_type": "PAN Card",
    "extracted_data": {
        "pan_number": "ABCDI2345F",
        "name": "Sample Kumar",
        "father_name": "",
        "date_of_birth": "01/01/2002"
    }
}

validator = DocumentValidator()

document = validator.validate(document)

print(document["validation"])