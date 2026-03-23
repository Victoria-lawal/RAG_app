import chromadb
from mistralai.client import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="ai_engineer")

mistral = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

while True:
    question = input("\nAsk a question (or type 'quit' to exit): ")
    if question.lower() == "quit":
        break

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = results["documents"][0][0]

    print(context)

    response = mistral.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "user", "content": f"Answer ONLY using the context below. If the answer isn't in the context, say 'I don't have that information.'\n\nContext: {context}\n\nQuestion: {question}"}
        ]
    )

    print("Answer:", response.choices[0].message.content)