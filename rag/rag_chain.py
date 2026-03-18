from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import EMBEDDING_MODEL, FAISS_INDEX_PATH
from qwen.qwen import ask_qwen

embedding = None
db = None


def rag_query(question):
    global embedding, db

    if db is None:
        if not Path(FAISS_INDEX_PATH).exists():
            raise FileNotFoundError(
                f"FAISS index not found at '{FAISS_INDEX_PATH}'. "
                "Run: python scripts/build_index.py"
            )
        if embedding is None:
            try:
                embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            except Exception as exc:
                raise RuntimeError(
                    "Failed to load embedding model. "
                    "Ensure internet access on first run, or set HF_ENDPOINT "
                    "(or HUGGINGFACE_ENDPOINT, e.g. https://hf-mirror.com), "
                    "or set EMBEDDING_MODEL to a local model path."
                ) from exc
        db = FAISS.load_local(
            str(FAISS_INDEX_PATH),
            embedding,
            allow_dangerous_deserialization=True,
        )

    docs = db.similarity_search(question, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer the question only based on the following context.

{context}

Question:
{question}
"""
    return ask_qwen(prompt)
