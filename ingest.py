import chromadb
from dotenv import load_dotenv

load_dotenv()

# Load your document
with open("ai engineer.txt", "r") as f:
    text = f.read()

# Split into chunks
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

chunks = chunk_text(text)
print(f"Created {len(chunks)} chunks")

# Store in ChromaDB
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="ai_engineer")

for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk],
        ids=[f"chunk_{i}"]
    )

print("Document stored successfully")