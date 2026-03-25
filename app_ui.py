import streamlit as st
import chromadb
from mistralai.client import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Medical Document Q&A")

mistral = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="ai_engineer")

question = st.text_input("Ask a question about the document:")

if question:
    results = collection.query(query_texts=[question], n_results=1)
    context = results["documents"][0][0]
    
    response = mistral.chat.complete(
        model="mistral-small-latest",
        messages=[{
            "role": "user",
            "content": f"Answer ONLY using the context below. If the answer isn't in the context, say 'I don't have that information.'\n\nContext: {context}\n\nQuestion: {question}"
        }]
    )
    
    st.write("**Answer:**", response.choices[0].message.content)
    st.write("**Retrieved context:**", context)