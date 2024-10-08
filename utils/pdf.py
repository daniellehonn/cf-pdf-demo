import os
import requests
import streamlit as st
from langchain_text_splitters import MarkdownHeaderTextSplitter


# Function to convert PDF to Markdown using ContextForce
def convert_pdf_to_md(pdf_file):
    # response = requests.post('https://r.contextforce.com/', files = {'file': ('uploaded_file.pdf', pdf_file, 'application/pdf')}, headers={'Accept': 'application/json', 'CF-Mode': 'auto', 'CF-Model': 'gpt-4o-mini', 'CF-OpenAI-Api-Key': os.getenv("OPENAI_API_KEY")})
    response = requests.post('https://r.contextforce.com/', files = {'file': ('uploaded_file.pdf', pdf_file, 'application/pdf')}, headers={'Accept': 'application/json'})
    if response.status_code == 200:
        print(response.text)
        return response.json()['markdown']
    else:
        st.error("Error converting PDF to Markdown")
        print(response.text)
        return None

def convert_pdf_to_html(pdf_file):
    response = requests.post('https://r.contextforce.com/', files = {'file': ('uploaded_file.pdf', pdf_file, 'application/pdf')}, headers={'Accept': 'text/html'})
    if response.status_code == 200:
        print(response.text)
        return response.text
    else:
        st.error("Error converting PDF to Markdown")
        print(response.text)
        return None

# Function to turn MD into Langchain Documents
def md_to_docs(md_text):
    print("md_to_docs")
    # MD splits
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
        ("#####", "Header 5"),
        ("######", "Header 6")
    ]

    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    return md_splitter.split_text(md_text)