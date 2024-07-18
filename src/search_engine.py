from pathlib import Path
import json

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.qparser import FuzzyTermPlugin, PrefixPlugin
from whoosh.index import open_dir


def create_index(index_dir, doc_dir):
    index_dir.mkdir(exist_ok=True)

    with open(doc_dir, 'r') as f:
        documents = json.load(f)

    schema = Schema(
        doc_id=ID(stored=True, unique=True),
        title=TEXT(stored=True),
        content=TEXT,
    )
    index = create_in(index_dir, schema)

    writer = index.writer()
    for doc in documents:
        writer.add_document(doc_id=doc['doc_id'], title=doc['title'], content=doc['content'])
    writer.commit()

    return index

def load_index(index_dir):
    index = open_dir(index_dir)
    return index

def create_query_parser(index):
    parser = MultifieldParser(["title", "content"], schema=index.schema)
    # parser = QueryParser("title", index.schema)
    parser.add_plugin(FuzzyTermPlugin())
    parser.add_plugin(PrefixPlugin())
    return parser


def search_index(index, query_str):
    parser = create_query_parser(index)
    query = parser.parse(query_str)
    results_list = []
    with index.searcher() as searcher:
        results = searcher.search(query, terms=True)
        for hit in results:
            results_list.append(hit.fields())

    return results_list


def print_search_results(index, results_list, documents):
    for hit in results_list:
        print(hit["title"], ":")
        print(documents[int(hit['doc_id'])]['content'])


def main():
    index_dir = Path('./indexes')
    doc_dir = Path('./data/documents.json')

    if index_dir.exists() :
        index = load_index(index_dir)
    else :
        index = create_index(index_dir, doc_dir)

    query_str = input("Enter your search query: ")
    results_list = search_index(index, query_str)

    with open(doc_dir, 'r') as f:
        documents = json.load(f)

    print_search_results(index, results_list, documents)


if __name__ == '__main__':
    main()