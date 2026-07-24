from sentence_transformers import SentenceTransformer
from config import Config


class EmbeddingService:
    """
    Handles text embeddings using Sentence Transformers.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            Config.EMBEDDING_MODEL
        )

    def generate_embedding(self, text: str):

        if not text.strip():
            return []

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()


embedding_service = EmbeddingService()