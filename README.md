# ChatBotVectorialDB 🚀

ChatBotVectorialDB es un backend profesional desarrollado con **FastAPI**, **LangChain** y **Pinecone**. Está diseñado para actuar como un asistente legal corporativo capaz de responder preguntas basadas exclusivamente en documentos PDF procesados mediante técnicas de RAG (Retrieval-Augmented Generation).

## 🌟 Características

- **Ingesta de Documentos**: Carga automática de múltiples PDFs desde una carpeta local.
- **Procesamiento de Texto**: División inteligente de texto con solapamiento para preservar el contexto.
- **Embeddings de Alta Calidad**: Uso de `text-embedding-3-large` de OpenAI con 2048 dimensiones.
- **Base de Datos Vectorial**: Integración con Pinecone para búsquedas semánticas rápidas.
- **Asistente Especializado**: Prompt de sistema configurado para actuar como un asistente legal corporativo estricto.
- **CORS Configurado**: Listo para ser consumido por aplicaciones Blazor o cualquier cliente frontend.
- **Floating Chat UI**: Interfaz web moderna e interactiva incluida en la carpeta `/frontend`.

## 🛠️ Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web.
- [LangChain](https://www.langchain.com/) - Orquestación de LLMs y RAG.
- [Pinecone](https://www.pinecone.io/) - Base de datos vectorial.
- [OpenAI](https://openai.com/) - LLM (GPT-4o-mini) y Embeddings.

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ChatBotVectorialDB.git
cd ChatBotVectorialDB
```

### 2. Configurar el Entorno Virtual
```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto y completa tus credenciales:
```env
OPENAI_API_KEY=tu_clave_de_openai
PINECONE_API_KEY=tu_clave_de_pinecone
PINECONE_INDEX_NAME=chatbotvectorialdb
PINECONE_ENVIRONMENT=us-east-1
DATABASE_URL=sqlite:///./sql_app.db
```

---

## 📖 Cómo Usar

### 1. Preparar los Datos
Coloca todos los archivos PDF que deseas indexar en la carpeta `./data`.

### 2. Ingestar Documentos
Ejecuta el script de ingesta para procesar los PDFs y subirlos a Pinecone:
```bash
python ingest.py
```

### 3. Iniciar el Servidor API
Lanza el backend con Uvicorn:
```bash
uvicorn app.main:app --reload
```
La API estará disponible en `http://localhost:8000`.

---

## 📡 Endpoints de la API

### `POST /api/v1/ask`
Realiza una pregunta al asistente legal.

**Request Body:**
```json
{
  "question": "¿Cuál es el procedimiento para X según el reglamento?"
}
```

**Response:**
```json
{
  "answer": "La respuesta generada por la IA...",
  "sources": [
    "documento_legal_1.pdf (página 5)",
    "reglamento_interno.pdf (página 12)"
  ]
}
```

---

## 🔒 Seguridad (CORS)
El backend está pre-configurado para permitir peticiones desde:
- `http://localhost:5000`
- `http://localhost:5001`

*(Puedes ajustar esto en `app/main.py`)*

---

## 🎨 Frontend: Floating Chat Component
Este repositorio incluye un componente de chat flotante desarrollado en **Blazor WebAssembly** diseñado para integrarse fácilmente con este backend.

Para más detalles, consulta la documentación en [/frontend/README.md](./frontend/README.md).

## 📄 Licencia
Este proyecto es de uso libre bajo la licencia MIT.
