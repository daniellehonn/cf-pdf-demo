import streamlit as st
from model_hub.config import PRICING
from model_hub.controller import ask_pdf
from vectorization import convert_pdf_to_md, get_and_store_embeddings, get_loaded_pdfs, search_pinecone
from io import BytesIO


# Function to generate response using LLM based on context
def generate_llm_response(context, query, selected_model):
    return ask_pdf(data={"context": context, "query": query}, selected_model=selected_model)


# Function to update session state when a new PDF is processed
def update_loaded_pdfs():
    st.session_state.loaded_pdfs = get_loaded_pdfs()

# Initialize session state for storing the list of PDFs
if 'loaded_pdfs' not in st.session_state:
    update_loaded_pdfs()


# Initialize Streamlit app
st.set_page_config(page_title="CF-PDF Demo")
st.title("ContextForce PDF Parser Demo 🍓")

# Sidebar components
st.sidebar.title("Web Scraper Settings")
model_selection = st.sidebar.selectbox("Select Model", options=list(PRICING.keys()), index=0)
uploaded_pdf = st.sidebar.file_uploader("Upload PDF File", type=['pdf'])
if uploaded_pdf:
    # st.sidebar.button("Extract PDF")
    if(st.sidebar.button("Extract PDF")):
        with st.spinner('Please wait... PDF data is being extracted.'):
            pdf_file = BytesIO(uploaded_pdf.read())
            markdown_text = convert_pdf_to_md(pdf_file)
            get_and_store_embeddings(markdown_text, uploaded_pdf.name)
            update_loaded_pdfs()
            st.success(f"Embeddings for {uploaded_pdf.name} stored in Pinecone.")

st.sidebar.markdown("---")
st.sidebar.title("Loaded PDFs")
# Dynamically load the updated PDFs list from session state
selected_pdf = st.sidebar.selectbox(
    "Select PDF",
    options=st.session_state.loaded_pdfs,
    index=0 if st.session_state.loaded_pdfs else -1
)


# Query Input
if selected_pdf:
    query = st.text_input("Enter your query:")

    if query:
        with st.spinner("Searching for relevant context..."):
            # Search Pinecone for relevant context
            search_results = search_pinecone(query, pdf_name=selected_pdf)
            # Get the context from the closest embeddings
            context = "\n".join([res.page_content for res in search_results])
        
        # Generate response using LLM based on the context
        with st.spinner("Generating response using LLM..."):
            response = generate_llm_response(context, query, selected_model=model_selection)
            st.success(f"{response}")
