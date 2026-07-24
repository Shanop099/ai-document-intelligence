# 📄 AI Document Intelligence System

An end-to-end AI-powered document intelligence pipeline that automatically classifies, extracts, validates, and enables semantic querying of business and identity documents using OCR, LLMs, vector search, and Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📤 Upload images or PDF documents
- 🔍 Automatic document type classification
- 📝 OCR for scanned documents
- 🤖 LLM-powered information extraction
- ✅ Rule-based data validation
- 📦 Structured JSON output
- 🔎 Semantic document search using Qdrant
- 💬 Chat with extracted documents using RAG
- 🌐 Interactive Streamlit interface

---

## 🗂 Supported Documents

- PAN Card
- Aadhaar Card
- GST Registration Certificate
- FSSAI License

---

## 🏗 Architecture

```text
                 Upload Document
                        │
                        ▼
                 Document Parser
                        │
         ┌──────────────┴──────────────┐
         │                             │
    Digital Document            Scanned Document
         │                             │
         │                         PaddleOCR
         │                             │
         └──────────────┬──────────────┘
                        ▼
             Document Classification
                 (Groq LLM)
                        │
                        ▼
             Information Extraction
                 (Groq LLM)
                        │
                        ▼
                 Data Validation
                        │
                        ▼
             Structured JSON Output
                        │
                        ▼
      Embedding Generation (BGE Small)
                        │
                        ▼
                 Qdrant Vector DB
                        │
                        ▼
                 RAG Chat Assistant
```

---

# 📁 Project Structure

```
AI-Document-Intelligence/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── backend/
│   ├── parser.py
│   ├── ocr.py
│   ├── classifier.py
│   ├── extractor.py
│   ├── validator.py
│   ├── embeddings.py
│   ├── qdrant_service.py
│   ├── rag_chat.py
│   ├── pipeline.py
│   └── utils.py
│
├── prompts/
│   ├── classifier_prompt.txt
│   ├── extraction_prompt.txt
│   └── chat_prompt.txt
│
├── uploads/
├── extracted_json/
└── qdrant_data/
```

---

# ⚙ Tech Stack

## Backend

- Python
- Streamlit
- Groq API
- Qdrant

## AI/ML

- PaddleOCR
- Sentence Transformers
- BAAI/bge-small-en-v1.5
- Llama-3.3-70B-Versatile

## Libraries

- OpenCV
- PyMuPDF
- Pillow
- NumPy
- Pandas
- Pydantic

---

# 📖 Pipeline

### 1. Document Upload

Accepts:

- PNG
- JPG
- JPEG
- PDF

---

### 2. Document Parsing

Determines

- Document type
- File extension
- Scanned/Digital document

---

### 3. OCR

Scanned documents are processed using PaddleOCR.

Digital PDFs directly extract embedded text.

---

### 4. Classification

The extracted text is sent to Groq LLM which identifies the document type.

Supported classes:

- PAN
- Aadhaar
- GST
- FSSAI
- Unknown

---

### 5. Information Extraction

The LLM extracts structured information according to predefined schemas.

Example:

```json
{
  "pan_number": "ABCDE1234F",
  "name": "John Doe",
  "father_name": "Richard Doe",
  "date_of_birth": "01/01/1990"
}
```

---

### 6. Validation

Each document undergoes rule-based validation.

Examples include:

- PAN format validation
- Aadhaar number validation
- GSTIN validation
- FSSAI license validation
- Missing field detection

---

### 7. Embedding Generation

Each extracted document is converted into semantic embeddings using:

```
BAAI/bge-small-en-v1.5
```

---

### 8. Vector Storage

Embeddings and metadata are stored in Qdrant for semantic retrieval.

---

### 9. RAG Chat

Users can ask natural language questions such as:

- What is the PAN number?
- Who owns this business?
- When does this license expire?
- Show the GST registration date.

The system retrieves relevant information from Qdrant before generating responses.

---

# 💻 Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Document-Intelligence.git

cd AI-Document-Intelligence
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_api_key

QDRANT_PATH=./qdrant_data

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

GROQ_MODEL=llama-3.3-70b-versatile
```

---

# ▶ Running the Project

```bash
streamlit run app.py
```

---

# 📷 Example Workflow

1. Upload a document

2. System classifies document type

3. OCR extracts text (if required)

4. LLM extracts structured information

5. Validator checks extracted fields

6. JSON is generated

7. Embeddings stored in Qdrant

8. Chat with the processed document

---

# 📊 Future Improvements

- Multi-document verification
- Passport support
- Driving License support
- Bank statement extraction
- Invoice understanding
- Confidence scores
- Batch document processing
- REST API
- User authentication
- Audit logging
- Docker deployment

---

# 👨‍💻 Author

**Ishan Gupta**

B.Tech Computer Science & Engineering

Indian Institute of Information Technology Nagpur

GitHub: https://github.com/Shanop099

---

# 📜 License

This project is intended for educational and demonstration purposes.
