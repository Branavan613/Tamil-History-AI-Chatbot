from groq import Groq
import os

from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from read_pdf import read_pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import conversational_retrieval



documents_folder = 'documents'

# Get a list of all PDF files in the folder
pdf_files = [f for f in os.listdir(documents_folder) if f.endswith('.pdf')]
pdf_strings = []

# Iterate through each PDF file and convert it to text
for pdf_file in pdf_files:
    pdf_path = os.path.join(documents_folder, pdf_file)
    pdf_text = read_pdf(pdf_path)
    pdf_strings.append(pdf_text)
    # print(f"Processed {pdf_file}")

pdf_strings = "/n/n".join(pdf_strings)
pdf_strings = pdf_strings.lower()

# # print(pdf_strings)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators = ["\n\n", "\n", " ", ""])
documents = text_splitter.split_text(pdf_strings)

# metadatas = [{"source": f"{i}-pl"} for i in range(len(documents))]

import ollama
import chromadb

client = chromadb.PersistentClient(path=".")
collection = client.create_collection(name="docs")

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embeddings(model="nomic-embed-text", prompt=d)
  embedding = response["embedding"]
  collection.add(
    ids=[str(i)],
    embeddings=[embedding],
    documents=[d]
  )

