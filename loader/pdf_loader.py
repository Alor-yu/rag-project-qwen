from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(path):
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.stat().st_size == 0:
        raise ValueError(f"PDF file is empty: {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()
    return documents
