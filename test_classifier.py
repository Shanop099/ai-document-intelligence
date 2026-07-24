from backend.classifier import DocumentClassifier

document = {
    "text": """
INCOME TAX DEPARTMENT
GOVT. OF INDIA

Permanent Account Number

ABCDI2345F

Sample Kumar

01/01/2002
"""
}

classifier = DocumentClassifier()

document = classifier.classify(document)

print(document["document_type"])