from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "BAAI/bge-small-en-v1.5"
    )

    QDRANT_PATH = os.getenv(
        "QDRANT_PATH",
        "./qdrant_data"
    )