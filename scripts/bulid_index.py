import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import DATA_PATH, FAISS_INDEX_PATH
from loader.pdf_loader import load_pdf
from vector_store.faiss_store import create_vector_store


def main():
    docs = load_pdf(DATA_PATH)
    db = create_vector_store(docs)
    db.save_local(str(FAISS_INDEX_PATH))
    print(f"Vector index created at: {FAISS_INDEX_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        raise SystemExit(f"Build index failed: {exc}")
