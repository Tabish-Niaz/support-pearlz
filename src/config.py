import os
from dotenv import load_dotenv

# .env file load karna
load_dotenv()

# API Keys aur Models
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY missing hai .env file mein!")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")

# Folders ki paths
KNOWLEDGE_BASE_DIR = "data/knowledge_base"
VECTOR_STORE_DIR = "data/vector_store"

# Chunking settings (Assignment manual ke mutabiq)
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150