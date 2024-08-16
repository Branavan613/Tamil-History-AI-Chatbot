
import os

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from read_pdf import read_pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import conversational_retrieval

pdf_strings = []
pdf_titles = []
pdf_authors = []

folders = ["first", "second"]
for folder in folders:
    documents_folder = os.path.join('documents', folder)
# Get a list of all PDF files in the folder
    pdf_files = [f for f in os.listdir(documents_folder) if f.endswith('.pdf')]
    # Iterate through each PDF file and convert it to text
    for i, pdf_file in enumerate(pdf_files):
        pdf_path = os.path.join(documents_folder, pdf_file)
        pdf_text, pdf_title, pdf_author = read_pdf(pdf_path, folder)
        pdf_strings.append(pdf_text)
        pdf_titles.append(pdf_title)
        pdf_authors.append(pdf_author)
    # print(f"Processed {pdf_file}")

assert len(pdf_strings) == len(pdf_titles) == len(pdf_authors), "Mismatch in the number of documents, titles, and authors"

import ollama
import chromadb

client = chromadb.PersistentClient(path=".")
collection = client.create_collection(name="docs")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""])

# Process each document
doc_id = 0
for doc_content, title, author in zip(pdf_strings, pdf_titles, pdf_authors):
    doc_content = doc_content.lower()
    documents = text_splitter.split_text(doc_content)
    
    for i, d in enumerate(documents):
        response = ollama.embeddings(model="nomic-embed-text", prompt=d)
        embedding = response["embedding"]
        
        # Create metadata dictionary
        metadata = {
            "title": title,
            "author": ", ".join(author),
            "chunk_index": i
        }
        
        # Add to collection with unique id for each chunk
        collection.add(
            ids=[f"{doc_id}_{i}"],
            embeddings=[embedding],
            documents=[d],
            metadatas=[metadata]
        )
    
    doc_id += 1
