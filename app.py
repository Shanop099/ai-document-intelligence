import json
import tempfile
from pathlib import Path

import streamlit as st

from backend.pipeline import DocumentPipeline
from backend.qdrant_service import qdrant_service
from backend.chat import chat_service


# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Intelligence")
st.write("Upload a document and extract structured information using AI.")

pipeline = DocumentPipeline()

# -----------------------------------------------------
# Session State Initialization
# -----------------------------------------------------

if "document" not in st.session_state:
    st.session_state.document = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------
# Upload Section
# -----------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:

    left, right = st.columns([1, 1])

    # ---------------------------------------------
    # Preview
    # ---------------------------------------------

    with left:

        st.subheader("📄 Uploaded Document")

        if uploaded_file.type.startswith("image"):

            st.image(
                uploaded_file,
                use_container_width=True
            )

        else:

            st.info("PDF uploaded successfully.")

    # ---------------------------------------------
    # Save Temporary File
    # ---------------------------------------------

    suffix = Path(uploaded_file.name).suffix

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as tmp:

        tmp.write(uploaded_file.getvalue())

        temp_path = tmp.name

    # ---------------------------------------------
    # Process Button
    # ---------------------------------------------

    with right:

        if st.button("🚀 Process Document", use_container_width=True):

            with st.spinner("Processing document..."):

                document = pipeline.process(temp_path)

                qdrant_service.store(document)

                st.session_state.document = document

                st.session_state.messages = []

            st.success("Document processed successfully!")

# -----------------------------------------------------
# Show Processed Document
# -----------------------------------------------------

if st.session_state.document:

    document = st.session_state.document

    st.divider()

    col1, col2 = st.columns(2)

    # ---------------------------------------------
    # Document Information
    # ---------------------------------------------

    with col1:

        st.subheader("📄 Document Information")

        st.metric(
            "Document Type",
            document["document_type"]
        )

        st.text_input(
            "Document ID",
            value=document["document_id"],
            disabled=True
        )

        st.text_input(
            "Filename",
            value=document["filename"],
            disabled=True
        )

        st.text_input(
            "Processed At",
            value=document["processed_at"],
            disabled=True
        )

    # ---------------------------------------------
    # Validation
    # ---------------------------------------------

    with col2:

        st.subheader("✅ Validation")

        if document["validation"]:

            for field, result in document["validation"].items():

                if result["valid"]:

                    st.success(
                        f"{field}: {result['message']}"
                    )

                else:

                    st.error(
                        f"{field}: {result['message']}"
                    )

        else:

            st.warning("No validation available.")

    # -------------------------------------------------

    st.divider()

    st.subheader("📋 Extracted Information")

    st.json(document["extracted_data"])

    # -------------------------------------------------

    st.divider()

    st.subheader("📥 Download JSON")

    with open(document["json_path"], "r", encoding="utf-8") as f:

        json_data = f.read()

    st.download_button(
        label="Download Extracted JSON",
        data=json_data,
        file_name=Path(document["json_path"]).name,
        mime="application/json",
        use_container_width=True
    )

    # -------------------------------------------------

    st.divider()

    st.subheader("💬 Chat with Document")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask a question about this document..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.spinner("Thinking..."):

            answer = chat_service.ask(
                question=prompt,
                document_id=document["document_id"]
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):

            st.markdown(answer)