# 🤖 AI Document Assistant

### Chat with your PDF & PowerPoint Documents using Google Gemini AI

# 📌 Overview

AI Document Assistant is a Retrieval-Augmented Generation (RAG) application that allows users to upload **PDF**, **PPT**, and **PPTX** documents and ask natural language questions about their contents.

The application extracts text, creates embeddings, stores them in a FAISS vector database, retrieves the most relevant information, and generates accurate answers using **Google Gemini AI**.

---

# ✨ Features

- 📄 Upload PDF, PPT, and PPTX documents
- 🤖 AI-powered question answering using Google Gemini
- 🔍 Semantic Search with FAISS
- 📚 Source-based responses
- 💬 Interactive Chat Interface
- 📊 Document Overview Panel
- 📈 Document Statistics
- ⚡ Fast Retrieval using Embeddings
- 🎨 Modern Responsive UI
- 🗂 Chat History
- 🧹 Clear Conversation

---

# 🛠 Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Flask
- Python

## AI Technologies

- Google Gemini API
- RAG
- Sentence Transformers
- FAISS Vector Database

## Libraries

- PyMuPDF
- python-pptx
- LangChain
- NumPy

---

# 📂 Project Structure

```text
AI-Document-Assistant/
│
├── app.py
├── chatbot.py
├── config.py
├── document_loader.py
├── embeddings.py
├── rag.py
├── text_chunker.py
├── vector_store.py
├── requirements.txt
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── uploads/
├── vector_db/
│
├── screenshots/
│   ├── home.png
│   ├── upload.png
│   ├── chat.png
│   └── sources.png
│
└── README.md
```

---

# ⚙ Installation

## Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/AI-Document-Assistant.git

cd AI-Document-Assistant
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create a .env File

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY

SECRET_KEY=your_secret_key
```

---

## Run the Application

```bash
python app.py
```

Visit

```
http://127.0.0.1:5000
```

---

# 🚀 Application Workflow

```text
User Uploads PDF/PPT
          │
          ▼
Document Loader
          │
          ▼
Text Extraction
          │
          ▼
Text Chunking
          │
          ▼
Embeddings Generation
          │
          ▼
FAISS Vector Database
          │
          ▼
User Question
          │
          ▼
Similarity Search
          │
          ▼
Relevant Chunks
          │
          ▼
Google Gemini AI
          │
          ▼
Final Answer
```

---

# 📦 Main Dependencies

- Flask
- Google Gemini API
- FAISS
- Sentence Transformers
- LangChain
- PyMuPDF
- python-pptx
- NumPy

---

# 🌟 Future Enhancements

- Multi-document Chat
- OCR Support
- Voice Input
- User Authentication
- Dark Mode
- Cloud Deployment
- Export Chat to PDF
- Drag & Drop Upload
- Image Understanding
- Multi-language Support

---

# 👩‍💻 Developer

**Anjali**

GitHub

https://github.com/anjaliaajagiya5277-creator

---

# ⭐ Support

If you found this project useful, consider giving it a **Star ⭐** on GitHub.

It helps others discover the project and motivates future improvements.

---
