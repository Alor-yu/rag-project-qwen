from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL


def create_vector_store(documents):

    try:
        embedding = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
    except Exception as exc:
        raise RuntimeError(
            "Failed to load embedding model. "
            "Ensure internet access on first run, or set HF_ENDPOINT "
            "(or HUGGINGFACE_ENDPOINT, e.g. https://hf-mirror.com), "
            "or set EMBEDDING_MODEL to a local model path."
        ) from exc

    db = FAISS.from_documents(documents, embedding)

    return db
