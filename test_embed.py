from backend.embeddings import embedding_service

text = """
Permanent Account Number

ABCDI2345F

Sample Kumar

01/01/2002
"""

embedding = embedding_service.generate_embedding(text)

print(type(embedding))
print(len(embedding))
print(embedding[:10])