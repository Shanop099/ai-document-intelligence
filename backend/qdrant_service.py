import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

from config import Config


class QdrantService:

    COLLECTION_NAME = "documents"

    def __init__(self):

        self.client = QdrantClient(path=Config.QDRANT_PATH)

        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.COLLECTION_NAME not in collection_names:

            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

    # ------------------------------------------
    # Store Document
    # ------------------------------------------

    def store(self, document):

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=document["embedding"],
            payload={
                "document_id": document["document_id"],
                "filename": document["filename"],
                "document_type": document["document_type"],

                "text": document["embedding_text"],
                "ocr_text": document["text"],

                "extracted_data": document["extracted_data"],
                "validation": document["validation"],

                "json_path": document["json_path"],
                "processed_at": document["processed_at"],
            },
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point],
        )

        return point.id

    # ------------------------------------------
    # Search All Documents
    # ------------------------------------------

    def search(self, query_embedding, limit=5):

        response = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_embedding,
            limit=limit,
            with_payload=True,
        )

        return response.points

    # ------------------------------------------
    # Search One Document
    # ------------------------------------------

    def search_document(
        self,
        query_embedding,
        document_id,
        limit=5,
    ):

        response = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_embedding,
            limit=limit,
            with_payload=True,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )

        return response.points

    # ------------------------------------------
    # Delete Collection
    # ------------------------------------------

    def reset(self):

        collections = self.client.get_collections().collections

        if any(c.name == self.COLLECTION_NAME for c in collections):
            self.client.delete_collection(self.COLLECTION_NAME)

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

    # ------------------------------------------
    # Close Client
    # ------------------------------------------

    def close(self):
        self.client.close()


qdrant_service = QdrantService()