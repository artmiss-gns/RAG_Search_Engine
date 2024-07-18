from src.llm import client
from src.search_engine import SearchEngine

search_engine = SearchEngine('./indexes', './data/documents.json')

keyword = input("what is the keyword you are searching for: ")
question = input("ask: ")
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
print(chat_completion.choices[0].message.content)