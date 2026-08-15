import os
import sys
import chromadb
# Ensure app package can be resolved
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
APP_ROOT = os.path.join(PROJECT_ROOT, "app")
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

from app.vectorstore.chroma_store import ChromaVectorStore

my_embedding_service = None

# store = ChromaVectorStore()
store = ChromaVectorStore()

query_embedding = [0.15] * 384

results = store.search(query_embedding)  # Pass None since we're directly providing the embedding

print(results)