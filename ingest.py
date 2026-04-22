import os
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

def ingest_documents(directory_path: str = "./data"):
    # 1. Initialize Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME", "chatbotvectorialdb")
    
    # Handle placeholder region
    region = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    if not region or "your_pinecone_environment" in region:
        region = "us-east-1"
    
    # Check if index exists, if not create it
    if index_name not in pc.list_indexes().names():
        print(f"Creating index: {index_name} in region {region}")
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region=region
            )
        )

    # 2. Load PDFs from directory
    print(f"Loading PDFs from: {directory_path}")
    loader = DirectoryLoader(
        directory_path,
        glob="./*.pdf",
        loader_cls=PyPDFLoader
    )
    data = loader.load()
    
    if not data:
        print("No PDF files found in the directory.")
        return

    # 3. Split text into chunks
    print(f"Splitting {len(data)} documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = text_splitter.split_documents(data)

    # 4. Generate embeddings and upload to Pinecone
    print(f"Generating embeddings and uploading {len(docs)} chunks to Pinecone...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        dimensions=1024
    )
    
    PineconeVectorStore.from_documents(
        docs,
        embeddings,
        index_name=index_name
    )
    
    print("Ingestion completed successfully!")

if __name__ == "__main__":
    ingest_documents()
