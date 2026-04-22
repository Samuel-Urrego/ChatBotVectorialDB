# 🛠️ PorciAI - Asistente Virtual de Soporte TI 🚀

¡Bienvenido a la rama **FAQTI**! Este proyecto ha sido transformado en un asistente inteligente especializado en **Soporte Técnico**, diseñado para resolver dudas de colaboradores de forma rápida, amable y precisa basándose en manuales de FAQ.

> "Resolviendo problemas técnicos con la velocidad del rayo y la precisión de la IA."

## ✨ Características de esta versión (FAQTI)

- **🔧 Especialista en TI**: Configurado con un System Prompt optimizado para dar soluciones paso a paso (reinicio de equipos, desbloqueo de cuentas, seguridad ante phishing, etc.).
- **📚 Base de Conocimiento**: Utiliza el índice `faq-ti-db` en Pinecone para consultar manuales técnicos internos.
- **🛡️ Seguridad Primero**: Instrucciones claras sobre cómo manejar links sospechosos y reportar incidentes de seguridad.
- **⚡ RAG de Alto Rendimiento**: Uso de `OpenAI text-embedding-3-large` con **1024 dimensiones** para una recuperación de información ultra-precisa.
- **📱 Telegram Ready**: Soporte total para consultas vía Telegram con mención de fuentes (metadatos de archivos PDF).

## 🛠️ Stack Tecnológico

| Tecnología | Propósito |
| :--- | :--- |
| **FastAPI** | API robusta y veloz |
| **LangChain** | Lógica de recuperación y generación (RAG) |
| **Pinecone** | Almacenamiento vectorial de FAQs |
| **OpenAI** | El cerebro (GPT-4o-mini) y Embeddings |
| **Render** | Despliegue en la nube simplificado |

---

## 🤖 Integración con Telegram

El bot de soporte técnico está a un mensaje de distancia:

1.  **Crea tu bot**: Obtén tu token con [@BotFather](https://t.me/botfather).
2.  **Configura el Webhook**:
    ```bash
    curl -X POST "https://api.telegram.org/bot<TU_TOKEN>/setWebhook?url=https://tu-app-en-render.com/telegram-webhook"
    ```
3.  **Manual de TI**: Asegúrate de haber realizado la ingesta de los PDFs de soporte en la carpeta `./data`.

---

## 🚀 Despliegue en Render

Esta rama (`FAQTI`) incluye correcciones críticas de dependencias (`pydantic`, `numpy`, `simsimd`) para un despliegue sin errores:

1.  Sube esta rama a GitHub.
2.  Crea un **Blueprint** en Render y selecciona este repositorio.
3.  **Configura tus env vars**:
    - `OPENAI_API_KEY`, `PINECONE_API_KEY`, `TELEGRAM_TOKEN`, etc.
    - Asegúrate de que `PINECONE_INDEX_NAME` sea `faq-ti-db`.

---

## 📖 Guía de Inicio Rápido

### 1. Instalación
```bash
git checkout FAQTI
pip install -r requirements.txt
```

### 2. Ingesta de FAQs 📂
Coloca tus manuales de soporte en `./data` y ejecuta:
```bash
python ingest.py
```

### 3. ¡A trabajar! 🛫
```bash
uvicorn main:app --reload
```

---

## 📄 Licencia
Este proyecto es de código abierto bajo la licencia **MIT**.

---
*Optimizado por PorciAI para el equipo de Soporte TI.*
