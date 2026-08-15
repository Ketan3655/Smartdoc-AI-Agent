from pathlib import Path

from app.services.parser import parse_document
from app.services.chunker import chunk_text
from app.services.embeddings import generate_embeddings

pages = parse_document(
    Path("uploads/sample.pdf")
)

chunks = chunk_text(pages)

embeddings = generate_embeddings(chunks)

print(f"Chunks: {len(chunks)}")
print(f"Embeddings: {len(embeddings)}")
print(f"Dimension: {len(embeddings[0])}")