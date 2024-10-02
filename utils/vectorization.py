# from pages.sources import add_source
from pinecone import Pinecone
from dotenv import load_dotenv
import os
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.pdf import convert_pdf_to_md, md_to_docs
from utils.webpage import convert_webpage_to_md
from utils.youtube import youtube_to_docs


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
    docs = md_to_docs(markdown_text)
    get_and_store_embeddings(docs, pdf_name, pdf_name.replace('.pdf', ''))
    # add_source(pdf_name)
    return None

# Function to index Youtube video transcripts
def index_youtube(youtube_url):
    print('Indexing Youtube video...')
    # Load Youtube video transcript
    docs = youtube_to_docs(youtube_url)
    get_and_store_embeddings(docs, youtube_url, "Youtube Video")
    # add_source(youtube_url)
    return None

# Function to index Webpage
def index_webpage(page_url):
    # Load Webpage
    markdown_text, title = convert_webpage_to_md(page_url)
    docs = md_to_docs(markdown_text)
    get_and_store_embeddings(docs, page_url, title)
    return None
    


# Function to get MD chunks and store them to Pinecone
def get_and_store_embeddings(docs, source, source_name):
    chunk_size = 1000
    chunk_overlap = 200
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Split
    splits = text_splitter.split_documents(docs)

    for id, text in enumerate(splits):
        if source_name == "Youtube Video":
            splits[id].metadata['source'] = f'{source}t={splits[id].metadata['start_seconds']}s'
            splits[id].metadata['source_name'] = splits[id].metadata['title']
        if source_name == "Youtube Video":
            splits[id].metadata['source'] = f'{source}t={splits[id].metadata['start_seconds']}s'
            splits[id].metadata['source_name'] = "website title"
        else:
            splits[id].metadata['source'] = f'{source}'
            splits[id].metadata['source_name'] = source_name
    
    # Add to vectorstore
    vectorstore.add_documents(
        documents=splits
    )
    return None

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


