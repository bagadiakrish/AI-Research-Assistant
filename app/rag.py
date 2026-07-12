import json
import faiss
import numpy as np
from google import genai
from sentence_transformers import SentenceTransformer
import os
from app.config import GEMINI_API_KEY

import fitz

def extract_text(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:

        text += page.get_text()
        text += "\n"

    return text
def create_chunks(text):

    chunk_size = 500

    chunks = []

    for i in range(0,len(text),chunk_size):

        chunk = text[i:i+chunk_size]

        chunks.append(chunk)

    with open(
        "data/chunks.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(chunks,file)

    return chunks
def create_embeddings(chunks):

    embeddings = embedding_model.encode(chunks)

    embeddings = np.array(
        embeddings
    ).astype("float32")

    return embeddings
def create_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    faiss.write_index(
        index,
        "models/faiss.index"
    )

    return index
def process_pdf(pdf_path):

    global chunks
    global index

    print("Step 1: Extracting text...")
    text = extract_text(pdf_path)

    print("Text length:", len(text))

    print("Step 2: Creating chunks...")
    chunks = create_chunks(text)

    print("Number of chunks:", len(chunks))

    print("Step 3: Creating embeddings...")
    embeddings = create_embeddings(chunks)

    print("Step 4: Creating FAISS index...")
    index = create_index(embeddings)

    print("Done!")

    return chunks, index
genai.configure(api_key=GEMINI_API_KEY)

llm = genai.GenerativeModel(
    "gemini-2.5-flash"
)
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chunks = []
index = None

if os.path.exists("data/chunks.json") and os.path.exists("models/faiss.index"):
    with open("data/chunks.json", "r", encoding="utf-8") as file:
        chunks = json.load(file)

    index = faiss.read_index("models/faiss.index")
def ask_pdf(question):
    if index is None or len(chunks) == 0:
        return "Please upload a PDF first."

    query_embedding = embedding_model.encode([question]).astype("float32")
    _, indices = index.search(query_embedding, 3)
    """
    Search the PDF using FAISS
    and answer using Gemini.
    """
    query_embedding=embedding_model.encode([question]).astype("float32")
    _,indices=index.search(query_embedding,3) 
    context=""
    for idx in indices[0]:
        context+=chunks[idx]
        context += "\n\n"
    prompt = f"""
    You are an AI Research Assistant.

    Answer ONLY from the provided context.

    If the answer is not present, say
    'I couldn't find that information in the document.'

    Context:
    {context}

    Question:
    {question}
    """
    try:
        response = llm.generate_content(prompt)
        return response.text

    except Exception as e:
        print(e)
        return "An error occurred while generating the response."