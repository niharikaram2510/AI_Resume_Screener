from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text):
    """
    Convert text into a semantic embedding.
    """

    embedding = model.encode(text)

    return embedding