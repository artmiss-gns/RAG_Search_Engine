from pathlib import Path
import json
import streamlit as st
from src.llm import client
from src.search_engine import SearchEngine

INDEX_DIR = Path("./indexes")
DOC_DIR = Path("./data/documents.json")

@st.cache_resource()
def create_engine():
    search_engine = SearchEngine(INDEX_DIR, DOC_DIR)
    if not INDEX_DIR.exists():
        st.success(f"Index created at {INDEX_DIR}")
        print("Creating index")
    else:
        st.success(f"Index loaded from {INDEX_DIR}")
        print("Loading index")
    return search_engine

search_engine = create_engine()


# @st.cache_data()
# def load_doc(doc_path):
#     with open(doc_path, "r") as f:
#         documents = json.load(f)
#     return documents

st.title("Whoosh Search Engine")
keyword = st.text_input("keyword:", value="", key="keyword")
question = st.text_input("Search:", value="", key="query_input")
search_button = st.button("Search")

# button to re-create the index
st.sidebar.header("Index Management")
with st.sidebar:
    if st.button("Re-create index"):
        search_engine.create_index() # ! should i update it ? or just recreate it 
        st.success(f"Index created at {INDEX_DIR}")


if search_button:
    results = search_engine(keyword)
    context = list(search_engine(keyword))
    context = [f"{result['title']}:{result['content']}" for result in context]
    prompt = f"""Answer ONLY based on the given Context.Don't add additional info, your only source is the context i give you.
Context: {context}
Question: {question}"""
    
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    answer = chat_completion.choices[0].message.content
    
    # chatbot answers
    st.header("Search Results")
    st.write(answer)
    