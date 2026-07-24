from backend.pipeline import DocumentPipeline
from backend.qdrant_service import qdrant_service
from backend.chat import chat_service

pipeline = DocumentPipeline()

document = pipeline.process("uploads/sample_pan.jpg")

qdrant_service.store(document)

print("\nDocument uploaded successfully.")
print("Document ID:", document["document_id"])

while True:

    question = input("\nAsk: ")

    if question.lower() == "exit":
        break

    answer = chat_service.ask(
        question=question,
        document_id=document["document_id"]
    )

    print("\nAI:")
    print(answer)

qdrant_service.close()