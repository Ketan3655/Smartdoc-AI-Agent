class DocumentChunker:
    def __init__(self, chunk_size=800, chunk_overlap=150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text):
        chunks = []

        start = 0

        while start < len(text):
            end = start + self.chunk_size

            chunks.append(text[start:end])

            start = end - self.chunk_overlap

        return chunks

    def chunk_document(self, pages):

        all_chunks = []

        for page in pages:

            page_chunks = self.split_text(page["text"])

            for chunk in page_chunks:

                all_chunks.append(
                    {
                        "text": chunk,
                        "page": page["page"]
                    }
                )

        return all_chunks


chunker = DocumentChunker()


def chunk_text(pages):
    return chunker.chunk_document(pages)