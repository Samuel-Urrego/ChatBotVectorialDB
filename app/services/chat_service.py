from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings

class ChatService:
    def __init__(self):
        # Initialize Pinecone client to check/create index
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index_name = settings.PINECONE_INDEX_NAME
        
        # Handle placeholder region from .env
        region = settings.PINECONE_ENVIRONMENT
        if not region or "your_pinecone_environment" in region:
            region = "us-east-1"

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1024,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region=region
                )
            )

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            dimensions=1024,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = PineconeVectorStore(
            index_name=index_name,
            embedding=self.embeddings,
            pinecone_api_key=settings.PINECONE_API_KEY
        )
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Custom strict prompt for IT Support Assistant
        template = """Eres el Asistente Virtual de Soporte TI de la Empresa. Tu propósito es ayudar a los colaboradores a resolver problemas técnicos de manera rápida y amable.

Reglas de oro:
1. Fidelidad al Contexto: Responde ÚNICAMENTE basándote en la información proporcionada en el manual de FAQ TI . Si la solución no se encuentra en el manual, no inventes una respuesta; indica amablemente que el usuario debe contactar directamente al área de soporte o esperar el tiempo de desbloqueo automático si aplica.
2. Instrucciones Claras: Proporciona soluciones paso a paso. Por ejemplo, si el equipo está lento, sugiere cerrar programas y reiniciar.
3. Seguridad Primero: Si el usuario reporta un correo o link sospechoso, enfatiza que NO debe abrirlo ni acceder a él.
4. Tono Profesional: Mantén un lenguaje técnico pero accesible, orientado a la resolución de problemas.

Ejemplos de respuestas basadas en tus fuentes:
- Si preguntan por contraseñas olvidadas: Indica que usen la opción "¿Olvidaste tu contraseña?" para recibir el enlace en su correo.
- Si preguntan por cuentas bloqueadas: Sugiere esperar unos minutos o solicitar el desbloqueo a TI.
- Si el equipo no enciende: Pide verificar energía y cables.

Contexto:
{context}

Pregunta: {question}
Respuesta de Soporte TI:"""
        
        self.QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

    def get_answer_with_sources(self, question: str) -> Dict[str, Any]:
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": self.QA_CHAIN_PROMPT},
            return_source_documents=True
        )
        
        result = qa_chain.invoke({"query": question})
        
        # Extract source metadata (like filename or page)
        sources = []
        for doc in result["source_documents"]:
            source_info = doc.metadata.get("source", "Unknown")
            page_info = doc.metadata.get("page", "")
            sources.append(f"{source_info} (página {page_info})" if page_info else source_info)
        
        # Unique sources
        unique_sources = list(set(sources))
        
        return {
            "answer": result["result"],
            "sources": unique_sources
        }

chat_service = ChatService()
