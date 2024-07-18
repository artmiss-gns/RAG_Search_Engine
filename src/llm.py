import os
from dotenv import load_dotenv, dotenv_values 
from groq import Groq

# loading variables from .env file
load_dotenv() 

print(os.environ.get("GROQ_API_KEY"))

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

prompt = input("Prompt: ")

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