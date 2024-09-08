# from groq import Groq
import os

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from read_pdf import read_pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import conversational_retrieval
import un_metadata
import fitz

def read_pdf(pdf_file):
    content = []
    with fitz.open(pdf_file) as file:
        for page in file: 
            content.append(page.get_text())
            
    content = ' '.join(content)
    return content

pdf_strings = []
documents_folder = 'un_documents'
# Get a list of all PDF files in the folder
pdf_files = [f for f in os.listdir(documents_folder) if f.endswith('.pdf')]
    # Iterate through each PDF file and convert it to text
for i, pdf_file in enumerate(pdf_files):
    pdf_path = os.path.join(documents_folder, pdf_file)
    pdf_strings.append(read_pdf(pdf_path))
    
    # print(f"Processed {pdf_file}")

import ollama
import chromadb

client = chromadb.PersistentClient(path=".")
collection = client.create_collection(name="un_docs")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""])

# Process each document
doc_id = 0
for doc_content, metatext in zip(pdf_strings, un_metadata.metadata):
    doc_content = doc_content.lower()
    documents = text_splitter.split_text(doc_content)
    
    for i, d in enumerate(documents):
        response = ollama.embeddings(model="nomic-embed-text", prompt=d)
        embedding = response["embedding"]
        
        # Create metadata dictionary
        metadata = {
            "title": metatext,
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