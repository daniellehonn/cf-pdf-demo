import requests
import re
import streamlit as st
from langchain_text_splitters import MarkdownHeaderTextSplitter


# Function to convert PDF to Markdown using ContextForce
def convert_webpage_to_md(page_url):
    print("convert_webpage_to_md")
    response = requests.get(f'https://r.contextforce.com/{page_url}')
    if response.status_code == 200:
        response_text = response.text
        # Step 1: Find the index of [MARKDOWN CONTENT]
        markdown_start = response_text.find("[CONTENT]") + len("[CONTENT]")
        # Step 2: Find the index of [OUTBOUND LINKS]
        metadata_start = response_text.find("[MATADATA]")
        # Step 3: Extract the substring between these two indices
        markdown_text = response_text[markdown_start:metadata_start]
        metadata_text = response_text[metadata_start:]
        # Step 4: Trim any leading or trailing whitespace
        markdown_text = markdown_text.strip()

        # Extract the Title field using regex
        title_match = re.search(r"Title:\s*(.*)", metadata_text)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = None

        return markdown_text, title
    else:
        st.error("Error converting Webpage to Markdown")
        print(response.text)
        return None
