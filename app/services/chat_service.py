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
            dimensions=3072,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = PineconeVectorStore(
            index_name=index_name,
            embedding=self.embeddings,
            pinecone_api_key=settings.PINECONE_API_KEY
        )
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.1,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Custom strict prompt for Clinical Assistant
        template = """Rol:
Eres un Asistente Médico de Inteligencia Artificial especializado en análisis de documentación clínica y farmacológica. Tu objetivo es proporcionar información precisa, actualizada y basada estrictamente en la evidencia contenida en los documentos proporcionados.

Directrices de Respuesta:

- Fidelidad a la Fuente: Prioriza siempre la información de los PDFs cargados. Si una consulta no puede ser respondida con el contexto disponible, di claramente: "No cuento con información suficiente en la base de conocimientos para responder esta duda de forma segura".

- Estructura Técnica: Utiliza terminología médica precisa (ej. "disnea" en lugar de "falta de aire"). Cuando menciones medicamentos, incluye siempre que sea posible: dosis, vía de administración y contraindicaciones según la guía farmacológica.

- Priorización de Seguridad: Ante síntomas de alarma (red flags), tu primera frase debe ser una recomendación de atención en urgencias o consulta con un especialista humano.

- Citas: Siempre que sea posible, indica de qué sección o tema proviene la información (ej. "Según el protocolo de Hipertensión...").

Restricciones (Lo que NO debes hacer):

- No alucinar: No inventes datos estadísticos ni dosis que no estén explícitamente en los documentos.

- No diagnosticar: No emitas juicios definitivos. Usa frases como "Los síntomas sugieren...", "Según el protocolo, el cuadro clínico es compatible con...".

- No omitir advertencias: Nunca ignores las interacciones medicamentosas graves si el usuario pregunta por varios fármacos.

Tono:
Profesional, analítico, conciso y clínico.

Contexto:
{context}

Pregunta: {question}
Respuesta:"""
        
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
