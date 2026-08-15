from pathlib import Path
from pypdf import PdfReader
from docx import Document


def parse_pdf(file_path: Path):
    """
    Returns:
    [
        {
            "page":1,
            "text":"..."
        }
    ]
    """

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text is None:
            text = ""

        pages.append(
            {
                "page": page_number,
                "text": text.strip()
            }
        )

    return pages


def parse_docx(file_path: Path):

    document = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

    return [
        {
            "page": 1,
            "text": text.strip()
        }
    ]


def parse_txt(file_path: Path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    return [
        {
            "page": 1,
            "text": text.strip()
        }
    ]


def parse_document(file_path: Path):

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return parse_pdf(file_path)

    elif suffix == ".docx":
        return parse_docx(file_path)

    elif suffix == ".txt":
        return parse_txt(file_path)

    raise ValueError(
        f"Unsupported file type: {suffix}"
    )