from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded.")

    def generate_embeddings(
        self,
        items
    ):

        texts = []

        for item in items:

            # Document chunk:
            # {"text": "...", "page": 1}
            if isinstance(item, dict):

                texts.append(
                    item["text"]
                )

            # Search query:
            # "What is this document about?"
            elif isinstance(item, str):

                texts.append(
                    item
                )

            else:

                raise TypeError(
                    "Each embedding item must "
                    "be a dictionary or string"
                )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        return [
            embedding.tolist()
            for embedding in embeddings
        ]


embedding_service = EmbeddingService()


def generate_embeddings(
    items
):

    return (
        embedding_service
        .generate_embeddings(
            items
        )
    )