import streamlit as st
from utils.navigation import make_sidebar
from utils.vectorization import index_pdf, index_youtube, index_webpage
from io import BytesIO

st.title("Upload Data...")
make_sidebar()
uploaded_pdf = st.file_uploader("Upload PDF File", type=['pdf'])
if uploaded_pdf:
    if st.button("Extract PDF"):
        with st.spinner('Please wait... PDF data is being extracted.'):
            pdf_file = BytesIO(uploaded_pdf.read())
            index_pdf(pdf_file, uploaded_pdf.name)
            st.success(f"PDF {uploaded_pdf.name} extracted successfully.")

st.markdown("---")

youtube_url = st.text_input("Extract from Youtube")
if youtube_url:
    if st.button("Extract Transcript"):
        with st.spinner('Please wait... transcript is being extracted.'):
            index_youtube(youtube_url)
            st.success(f"Transcript extracted successfully.")

st.markdown("---")

page_url = st.text_input("Extract from a webpage")
if page_url:
    if st.button("Extract Page"):
        with st.spinner('Please wait... webpage is being extracted.'):
            index_webpage(page_url)
            st.success(f"Webpage extracted successfully.")
