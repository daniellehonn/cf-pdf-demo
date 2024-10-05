import os
import requests
import streamlit as st
from langchain_text_splitters import MarkdownHeaderTextSplitter


# Function to convert PDF to Markdown using ContextForce
def convert_pdf_to_md(pdf_file):
    response = requests.post('https://r.contextforce.com/', files = {'file': ('uploaded_file.pdf', pdf_file, 'application/pdf')}, headers={'CF-Result-Format': 'markdown', 'CF-Mode': 'auto', 'CF-Model': 'gpt-4o-mini', 'CF-OpenAI-Api-Key': os.getenv("OPENAI_API_KEY")})
    if response.status_code == 200:
        print(response.text)
        response_text = response.text
        # Step 1: Find the index of [MARKDOWN CONTENT]
        markdown_start = response_text.find("[MARKDOWN CONTENT]") + len("[MARKDOWN CONTENT]")
        # Step 2: Find the index of [OUTBOUND LINKS]
        outbound_links_start = response_text.find("[OUTBOUND LINKS]")
        # Step 3: Extract the substring between these two indices
        markdown_text = response_text[markdown_start:outbound_links_start]
        # Step 4: Trim any leading or trailing whitespace
        markdown_text = markdown_text.strip()
        # markdown_text = response.text.split('"markdown": "')[1].split('", "')[0]
        return markdown_text
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