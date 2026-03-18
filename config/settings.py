import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "").strip()
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-turbo")
HUGGINGFACE_ENDPOINT = os.getenv(
    "HUGGINGFACE_ENDPOINT",
    os.getenv("HF_ENDPOINT", ""),
).strip()
if HUGGINGFACE_ENDPOINT:
    os.environ["HF_ENDPOINT"] = HUGGINGFACE_ENDPOINT

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

FAISS_INDEX_PATH = BASE_DIR / "faiss_index"

DEFAULT_DATA_PATH = BASE_DIR / "data" / "knowledge.pdf"
DATA_PATH = Path(os.getenv("DATA_PATH", str(DEFAULT_DATA_PATH))).expanduser()
if not DATA_PATH.is_absolute():
    DATA_PATH = BASE_DIR / DATA_PATH

if not DATA_PATH.exists():
    pdf_candidates = sorted((BASE_DIR / "data").glob("*.pdf"))
    if len(pdf_candidates) == 1:
        DATA_PATH = pdf_candidates[0]


def get_dashscope_api_key():
    return os.getenv("DASHSCOPE_API_KEY", DASHSCOPE_API_KEY).strip()
