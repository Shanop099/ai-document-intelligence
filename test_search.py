from backend.embeddings import embedding_service
from backend.qdrant_service import qdrant_service

query = "What is the PAN number?"

embedding = embedding_service.generate_embedding(query)

results = qdrant_service.search(embedding)

print(f"\nFound {len(results)} result(s)\n")

if not results:
    print("No documents found.")
else:

    payload = results[0].payload

    for key, value in payload.items():
        print(f"{key}:")
        print(value)
        print("-" * 60)

qdrant_service.close()