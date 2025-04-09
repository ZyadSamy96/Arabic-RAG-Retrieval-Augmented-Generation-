# Arabic RAG (Retrieval-Augmented Generation)

![RAG System](https://img.shields.io/badge/Language-Arabic-blue) ![Dockerized](https://img.shields.io/badge/Deployment-Docker-green)

**Author**: Zyad Samy

---

## 📌 Project Overview

**Arabic RAG** is an end-to-end system for Retrieval-Augmented Generation (RAG) tailored for Arabic documents. It extracts textual and visual information from PDFs, preprocesses and encodes them using the CLIP model, stores embeddings in a vector database, and supports real-time question answering over the ingested content.

---

## 🧠 Problem Statement

RAG enhances LLM outputs by grounding them in real documents to reduce hallucinations. However, working with Arabic content introduces challenges such as:
- OCR limitations in Arabic script.
- Noise and inconsistencies in scanned documents.
- LLM hallucinations when information is not retrieved accurately.

---

## 📥 Data Loading

### 📝 Text Extraction
- **PyPDF2** and **pdfplumber** were tested but failed with Arabic.
- **Tesseract OCR** was selected for its speed and accuracy with Arabic.
- **EasyOCR** was also tested, but slow on CPU.

### 🖼 Image Extraction
- Custom algorithm used to extract and process images from PDFs when libraries failed.

---

## 🧹 Preprocessing

- Remove noisy characters (e.g., repeated "لا").
- Strip non-Arabic symbols and single-letter artifacts.
- Normalize Arabic diacritics and characters.
- Clean metadata and reference sections.

---

## 🔍 Model: CLIP

- Uses **CLIP (Contrastive Language–Image Pretraining)** for joint vision-language embedding.
- Handles both text and image embeddings for document segments.

---

## 🧬 Vector Database

- **Qdrant** selected for:
  - High-speed similarity search
  - Open-source and easy integration
  - Efficient memory usage compared to manual .npy + index files

---

## 🚀 Deployment

- Fully **Dockerized** for ease of deployment.
- **FastAPI** endpoints:
  - `/download`: Downloads PDFs from Google Drive
  - `/process_pdf`: Extracts and uploads embeddings to Qdrant
  - `/query_document`: Queries Qdrant for relevant content

---

## 📊 Evaluation

- **Retrieval Metrics**: MRR, F1-Score
- **OCR Evaluation**
- **Generation Quality**: Human fluency assessment
- **Performance**: Response time & throughput

---

## 🎯 Conclusion

This system provides a scalable and efficient solution to enable Arabic document understanding using RAG. It supports multimodal inputs (text + image), custom preprocessing, and real-time querying using vector databases.

---

## 📦 Tech Stack

- Python 3.9
- Tesseract OCR
- CLIP (Hugging Face)
- Qdrant
- FastAPI
- Docker

---

## 🛠 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/arabic-rag.git
cd arabic-rag

# Build the Docker image
docker build -t arabic-rag .

# Run the container
docker run -p 8000:8000 arabic-rag
