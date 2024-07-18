from pathlib import Path
import json

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.qparser import FuzzyTermPlugin, PrefixPlugin

class SearchEngine:
    def __init__(self, index_dir, doc_dir):
        self.index_dir = Path(index_dir)
        self.doc_dir = Path(doc_dir)
        self.index = None
        with open(self.doc_dir, 'r') as f:
             self.documents = json.load(f)

    def create_index(self):
        self.index_dir.mkdir(exist_ok=True)
        # re-open docs, since it might have been modified
        with open(self.doc_dir, 'r') as f:
            self.documents = json.load(f)

        schema = Schema(
            doc_id=ID(stored=True, unique=True),
            title=TEXT(stored=True),
            content=TEXT,
        )
        self.index = create_in(self.index_dir, schema)

        writer = self.index.writer()
        for doc in self.documents:
            writer.add_document(doc_id=doc['doc_id'], title=doc['title'], content=doc['content'])
        writer.commit()

    def load_index(self):
        self.index = open_dir(self.index_dir)

    def create_query_parser(self):
        parser = MultifieldParser(["title", "content"], schema=self.index.schema)
        parser.add_plugin(FuzzyTermPlugin())
        parser.add_plugin(PrefixPlugin())
        return parser

    def search_index(self, query_str):
        parser = self.create_query_parser()
        query = parser.parse(query_str)
        results_list = []
        with self.index.searcher() as searcher:
            results = searcher.search(query, terms=True)
            for hit in results:
                results_list.append(hit.fields())
        return results_list


    def __call__(self):
        if not self.index_dir.exists():
            self.create_index()
        else:
            self.load_index()

        query_str = input("Enter your search query: ")
        results_list = self.search_index(query_str)

        for hit in results_list:
            yield {
                'title': hit["title"],
                'content': self.documents[int(hit['doc_id'])]['content']
            }


if __name__ == '__main__':
    search_engine = SearchEngine('./indexes', './data/documents.json')
    print(*list(search_engine()))