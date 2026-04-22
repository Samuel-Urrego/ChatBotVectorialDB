from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings

class ChatService:
    def __init__(self):
        # Initialize Pinecone client
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index_name = settings.PINECONE_INDEX_NAME
        
        region = settings.PINECONE_ENVIRONMENT
        if not region or "your_pinecone_environment" in region:
            region = "us-east-1"

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=2048,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region=region)
            )

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            dimensions=2048,
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
        
        # Custom prompt
        template = """Eres un asistente legal corporativo. Responde ÚNICAMENTE basándote en el contexto proporcionado. 
Si la respuesta no está en el reglamento, di que no lo sabes.

Contexto:
{context}

Pregunta: {input}
Respuesta Legal:"""
        
        self.QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "input"],
            template=template,
        )

    def get_answer_with_sources(self, question: str) -> Dict[str, Any]:
        # Legacy method using RetrievalQA
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": self.QA_CHAIN_PROMPT.rename_parameter("input", "question")},
            return_source_documents=True
        )
        result = qa_chain.invoke({"query": question})
        sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        return {"answer": result["result"], "sources": list(set(sources))}

    async def get_answer_stream(self, question: str):
        # Modern LCEL implementation (more resilient to import errors)
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Create the LCEL chain
        rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | self.QA_CHAIN_PROMPT
            | self.llm
            | StrOutputParser()
        )
        
        async for chunk in rag_chain.astream(question):
            yield chunk

chat_service = ChatService()
