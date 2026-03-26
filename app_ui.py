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

with open("neural_engineering.txt", "r") as f:
    text = f.read()

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

if collection.count() == 0:
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        collection.add(documents=[chunk], ids=[f"chunk_{i}"])
        
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