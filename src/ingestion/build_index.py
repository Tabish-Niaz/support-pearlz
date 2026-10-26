import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import sys
import warnings

# LangChain warnings hide karne ke liye
warnings.filterwarnings("ignore")

# Config file load karna
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.config as config

def build_index():
    print("🚀 Ingestion Pipeline Started...")
    print(f"Reading files from: {config.KNOWLEDGE_BASE_DIR}")
    
    documents = []
    
    # 1. Load Data
    for filename in os.listdir(config.KNOWLEDGE_BASE_DIR):
        filepath = os.path.join(config.KNOWLEDGE_BASE_DIR, filename)
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext == ".md":
                loader = UnstructuredMarkdownLoader(filepath)
                docs = loader.load()
                for doc in docs: doc.metadata['source'] = filename
                documents.extend(docs)
                print(f"✅ Loaded: {filename}")
            elif ext == ".csv":
                loader = CSVLoader(filepath)
                docs = loader.load()
                for doc in docs: doc.metadata['source'] = filename
                documents.extend(docs)
                print(f"✅ Loaded: {filename}")
        except Exception as e:
            print(f"❌ Failed to load {filename}: {e}")

    if not documents:
        print("⚠️ Koi file read nahi hui. Data folder check karein.")
        return

    # 2. Split Text (Chunking)
    print("\n✂️ Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    print(f"📊 Total Chunks Generated: {len(chunks)}")

    # 3. Create Embeddings & Save to Vector Database
    print("\n🧠 Generating Embeddings aur Vector Store save ho raha hai (Isme 1-2 minute lag sakte hain)...")
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.VECTOR_STORE_DIR
    )
    
    print("\n🎉 Vector database successfully ban gaya hai!")
    print(f"Index yahan save hua: {config.VECTOR_STORE_DIR}")

if __name__ == "__main__":
    build_index()