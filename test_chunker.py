from pathlib import Path

from app.services.parser import parse_document
from app.services.chunker import chunk_text

pages = parse_document(
    Path("uploads/sample.pdf")
)

chunks = chunk_text(pages)

print(chunks[0])
print()

print(f"Total chunks: {len(chunks)}")