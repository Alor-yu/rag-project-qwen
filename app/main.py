import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from rag.rag_chain import rag_query

st.set_page_config(page_title="RAG Knowledge Base Q&A")
st.title("RAG Knowledge Base Q&A")

question = st.text_input("Enter your question:")

if question:
    with st.spinner("Generating answer..."):
        try:
            answer = rag_query(question)
        except FileNotFoundError:
            st.error("Vector index not found. Run: python scripts/build_index.py")
        except Exception as exc:
            st.error(f"Request failed: {exc}")
        else:
            st.write("Answer:")
            st.write(answer)
