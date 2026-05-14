<h1 align="center">ChatBotVectorialDB // Corporate Legal AI</h1>
<p align="center">
  <strong>Backend profesional de orquestación RAG para asistencia legal corporativa.</strong>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat-square&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/LangChain-v0.1-1C3C3C?style=flat-square" alt="LangChain" />
  <img src="https://img.shields.io/badge/Pinecone-VectorDB-000000?style=flat-square" alt="Pinecone" />
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai" alt="OpenAI" />
</p>
ChatBotVectorialDB es un motor de backend de alto rendimiento desarrollado con **FastAPI**, **LangChain** y **Pinecone**. Implementa técnicas avanzadas de **RAG (Retrieval-Augmented Generation)** para transformar documentos legales estáticos en un asistente corporativo inteligente y estricto.
## 🌟 Key Features
- **Automated Ingestion**: Ingesta masiva de PDFs con fragmentación inteligente y solapamiento de contexto.
- **High-Dim Embeddings**: Procesamiento vectorial mediante `text-embedding-3-large` (2048 dims).
- **Strict Logic**: Prompt de sistema blindado para comportamiento legal corporativo profesional.
- **Scale-Ready**: Integración nativa con Pinecone Serverless y CORS pre-configurado para clientes modernos.
## 🛠️ Logic Stack
| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI |
| **Orchestrator** | LangChain |
| **Vector Engine** | Pinecone |
| **Model** | GPT-4o-mini |
| **Embeddings** | OpenAI text-embedding-3-large |
---
## 🚀 Deployment & Config
### 1. Environment Setup
```bash
# Clone the logic
git clone https://github.com/tu-usuario/ChatBotVectorialDB.git
cd ChatBotVectorialDB
# Activate virtual environment
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
2. Signal Transmission (Env Vars)
Crea un archivo .env con los siguientes parámetros de sistema:

env
OPENAI_API_KEY=tu_clave_de_openai
PINECONE_API_KEY=tu_clave_de_pinecone
PINECONE_INDEX_NAME=chatbotvectorialdb
📖 System Operations
Ingestion Mode
Procesa los documentos en la carpeta ./data y sincroniza con la base de datos vectorial:

bash
python ingest.py
API Execution
Lanza el servidor de producción:

bash
uvicorn app.main:app --reload
📡 API Endpoints
POST /api/v1/ask
Transmite una consulta al núcleo de IA.

Request:

json
{
  "question": "¿Cuál es el procedimiento para X según el reglamento?"
}
Response:

json
{
  "answer": "La respuesta generada por la IA...",
  "sources": ["doc_1.pdf (pág 5)", "reglamento.pdf (pág 12)"]
}
