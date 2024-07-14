from pathlib import Path
import json
import streamlit as st
from search_engine import create_index, load_index, search_index

INDEX_DIR = Path("./indexes")
DOC_DIR = Path("./data/documents.json")

@st.cache_resource()
def set_index():
    if not INDEX_DIR.exists():
        index = create_index(INDEX_DIR, DOC_DIR)
        st.success(f"Index created at {INDEX_DIR}")
        print("Creating index")
    else:
        index = load_index(INDEX_DIR)
        st.success(f"Index loaded from {INDEX_DIR}")
        print("Loading index")
    return index

@st.cache_data()
def load_doc(doc_path):
    with open(doc_path, "r") as f:
        documents = json.load(f)
    return documents

st.title("Whoosh Search Engine")
query_input = st.text_input("Search:", value="")
search_button = st.button("Search")

# button to re-create the index
st.sidebar.header("Index Management")
with st.sidebar:
    if st.button("Re-create index"):
        index = create_index(INDEX_DIR, DOC_DIR)
        st.success(f"Index created at {INDEX_DIR}")


if search_button:
    index = set_index()
    results = search_index(index, query_input)
    documents = load_doc(DOC_DIR)

    # Display the search results
    st.header("Search Results")
    for hit in results:
        st.write(f"**{hit['title']}**")
        st.write(documents[int(hit['doc_id'])]['content'])
        st.write("---")
