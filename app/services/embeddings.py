from fastembed import TextEmbedding


class EmbeddingService:

    def __init__(self):
        print("Loading lightweight embedding model...")

        self.model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

        print("Embedding model loaded.")

    def generate_embeddings(self, items):

        texts = []

        for item in items:

            # Document chunk
            if isinstance(item, dict):
                texts.append(item["text"])

            # Search query
            elif isinstance(item, str):
                texts.append(item)

            else:
                raise TypeError(
                    "Each embedding item must be a dictionary or string"
                )

        embeddings = self.model.embed(texts)

        return [
            embedding.tolist()
            for embedding in embeddings
        ]


embedding_service = EmbeddingService()


def generate_embeddings(items):

    return embedding_service.generate_embeddings(items)