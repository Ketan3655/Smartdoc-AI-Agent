from app.services.parser import parse_document
from pathlib import Path

pages = parse_document(
    Path("uploads/Ankit_Prajapati_Resume.pdf")
)

print(pages[0])