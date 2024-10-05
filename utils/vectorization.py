# from pages.sources import add_source
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import urllib.parse
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.pdf import convert_pdf_to_md, md_to_docs
from utils.webpage import convert_webpage_to_md
from utils.youtube import youtube_to_docs
from utils.r2_upload import upload_file_to_r2, upload_md_to_r2
from utils.d1 import add_source


load_dotenv()

# Initialize Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# use default tf-idf values
# bm25_encoder = BM25Encoder().default()

# Initialize Pinecone
pc = Pinecone(pinecone_api_key=os.getenv("PINECONE_API_KEY"), environment="us-east-1")
index = pc.Index(host="https://cf-pdf-demo-902dea1.svc.aped-4627-b74a.pinecone.io")
vectorstore = PineconeVectorStore(index, embeddings)


# Function to index PDFs
def index_pdf(pdf_file, pdf_name):
    # Load PDF
    markdown_text = convert_pdf_to_md(pdf_file)
    upload_md_to_r2(markdown_text, pdf_name.replace('.pdf', ''))
    docs = md_to_docs(markdown_text)
    get_and_store_embeddings(docs, "pdf", f"https://r2.contextforce.com/{pdf_name}", pdf_name.replace('.pdf', ''))
    return None

# Function to index Youtube video transcripts
def index_youtube(youtube_url):
    print('Indexing Youtube video...')
    # Load Youtube video transcript
    docs = youtube_to_docs(youtube_url)
    get_and_store_embeddings(docs, "youtube", youtube_url)
    return None

# Function to index Webpage
def index_webpage(page_url):
    # Load Webpage
    markdown_text, title = convert_webpage_to_md(page_url)
    upload_md_to_r2(markdown_text, title)
    docs = md_to_docs(markdown_text)
    get_and_store_embeddings(docs, "webpage", page_url, title)
    return None
    


# Function to get MD chunks and store them to Pinecone
def get_and_store_embeddings(docs, source_type, source, source_name=None):
    print("get_and_store_embeddings")
    chunk_size = 1000
    chunk_overlap = 200
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Split
    splits = text_splitter.split_documents(docs)
    for id, text in enumerate(splits):
        if source_type == "youtube":
            splits[id].metadata['source'] = f'{source}t={splits[id].metadata['start_seconds']}s'
            source_name = splits[id].metadata['title']
            md_file = source
        else:
            if source_type == "pdf":
                splits[id].metadata['source'] = f'{source}'
            elif source_type == "webpage":
                splits[id].metadata['source'] = f'{source}#:~:text={urlEncode(splits[id].page_content)}'
            md_file = f"https://r2.contextforce.com/{urllib.parse.quote(source_name.replace(' ', '_'), safe="_-.")}.md"

        splits[id].metadata['source_name'] = source_name
    
    # Add to vectorstore
    vectorstore.add_documents(
        documents=splits
    )

    md_file = ""
    if source_type == "youtube":
        md_file = source
    else:
        md_file = f"https://r2.contextforce.com/{urllib.parse.quote(source_name.replace(' ', '_'), safe="_-.")}.md"

    add_source(source_name, source_type, source, md_file, len(splits))
    print(f"Successfully indexed {len(splits)} chunks from {source_name} and stored to D1/Pinecone")

    return None

def urlEncode(text):
    words = text.split()  
    first_5_words = words[:5]  
    last_5_words = words[-5:]
    return f'{'%20'.join(first_5_words)},{'%20'.join(last_5_words)}'

# Function to search Pinecone for relevant embeddings
def vector_similarity_search(query):
    result = vectorstore.similarity_search(query, k=4)
    return result


def pinecone_remove_source(source):
    # Query the index for documents that match the metadata
    # Create an empty query vector of 768 dimensions
    empty_query_vector = [0.0] * 768  # List of zeros
    query_results = index.query(  # Adjust the parameters as needed
        vector = empty_query_vector,
        filter={'source': source},
        top_k=1000
    )

    # Get the IDs of the documents to delete
    document_ids_to_delete = [match['id'] for match in query_results['matches']]

    if document_ids_to_delete:
        # Delete the documents from the index
        index.delete(ids=document_ids_to_delete)
    return None

def pinecone_remove_all():
    # Query the index for documents that match the metadata
    # Create an empty query vector of 768 dimensions
    empty_query_vector = [0.0] * 768  # List of zeros
    query_results = index.query(  # Adjust the parameters as needed
        vector = empty_query_vector,
        top_k=1000
    )

    # Get the IDs of the documents to delete
    document_ids_to_delete = [match['id'] for match in query_results['matches']]

    if document_ids_to_delete:
        # Delete the documents from the index
        index.delete(ids=document_ids_to_delete)
    return None


