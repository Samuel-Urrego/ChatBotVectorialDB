import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

def ingest_documents(directory_path: str = "./data"):
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME", "chatbot-medico-db")
    
    # 1. Configuración de dimensiones (Ajustado a 3072 para máxima precisión médica)
    dimensions = 3072 
    region = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

    if index_name not in pc.list_indexes().names():
        print(f"Creando índice: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=dimensions,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region=region)
        )

    # 2. Carga con PyPDFLoader (ideal para manuales técnicos)
    print(f"Cargando manuales médicos desde: {directory_path}")
    loader = DirectoryLoader(
        directory_path,
        glob="**/*.pdf", # Busca también en subcarpetas
        loader_cls=PyPDFLoader
    )
    data = loader.load()
    
    # 3. Splitting optimizado para protocolos y dosis
    # Aumentamos el overlap para no perder contexto en tablas o listas
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True,
    )
    docs = text_splitter.split_documents(data)

    # 4. Embeddings de alta resolución
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        dimensions=dimensions 
    )
    
    # 5. Carga masiva (Batch upload)
    print(f"Subiendo {len(docs)} fragmentos a Pinecone...")
    PineconeVectorStore.from_documents(
        docs,
        embeddings,
        index_name=index_name
    )
    
    print("¡Ingesta médica completada con éxito!")

if __name__ == "__main__":
    ingest_documents()