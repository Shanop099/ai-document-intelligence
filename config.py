import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class Config:
    GROQ_API_KEY = GROQ_API_KEY

    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    QDRANT_PATH = os.getenv("QDRANT_PATH", "./qdrant_data")