from pinecone import Pinecone
from openai import OpenAI
import requests
import streamlit as st
from dotenv import load_dotenv
import os
import re
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter


load_dotenv()

# Initialize Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Initialize Pinecone
pc = Pinecone(pinecone_api_key=os.getenv("PINECONE_API_KEY"), environment="us-east-1")
index = pc.Index(host="https://cf-pdf-demo-902dea1.svc.aped-4627-b74a.pinecone.io")
vectorstore = PineconeVectorStore(index, embeddings)


# Function to convert PDF to Markdown using ContextForce
def convert_pdf_to_md(pdf_file):
    response = requests.post('https://r.contextforce.com/', files = {'file': ('uploaded_file.pdf', pdf_file, 'application/pdf')}, headers={'resultFormat': 'json'})
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()
        # Access the 'text' -> 'markdown' field
        markdown_text = response_json.get('text', {}).get('markdown', "")
        return markdown_text
    else:
        st.error("Error converting PDF to Markdown")
        print(response.text)
        return None


# Function to get MD chunks and store them to Pinecone
def get_and_store_embeddings(text, pdf_name):
    # MD splits
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]
    text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_chunks = text_splitter.split_text(text)

    # Char-level splits
    # from langchain_text_splitters import RecursiveCharacterTextSplitter

    # chunk_size = 250
    # chunk_overlap = 30
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=chunk_size, chunk_overlap=chunk_overlap
    # )
    vectorstore.add_texts([chunk.page_content for chunk in md_header_chunks], namespace=pdf_name)

    return None

# Function to search Pinecone for relevant embeddings
def search_pinecone(query, pdf_name=None):
    results = vectorstore.similarity_search(query, namespace=pdf_name)
    return results

# Return pdfs already loaded into Pinecone
def get_loaded_pdfs():
    return index.describe_index_stats().namespaces.keys()
