import streamlit as st
import time
from utils.navigation import make_sidebar
from utils.vectorization import index_pdf, index_youtube, index_webpage
from utils.r2_upload import upload_file_to_r2
from io import BytesIO

st.title("Upload Data...")
make_sidebar()
uploaded_pdf = st.file_uploader("Upload PDF File", type=['pdf'])
if uploaded_pdf:
    if st.button("Extract PDF"):
        with st.spinner('Please wait... PDF data is being extracted.'):
            pdf_data = uploaded_pdf.read()
            upload_file_to_r2(BytesIO(pdf_data), uploaded_pdf.name)
            index_pdf(BytesIO(pdf_data), uploaded_pdf.name)

        st.success(f"PDF {uploaded_pdf.name} extracted successfully.")
        time.sleep(2)
        st.rerun()


st.markdown("---")

youtube_url = st.text_input("Extract from Youtube")
if youtube_url:
    if st.button("Extract Transcript"):
        with st.spinner('Please wait... transcript is being extracted.'):
            index_youtube(youtube_url)
            
        st.success(f"Transcript extracted successfully.")
        time.sleep(2)
        st.rerun()

st.markdown("---")

page_url = st.text_input("Extract from a webpage")
if page_url:
    if st.button("Extract Page"):
        with st.spinner('Please wait... webpage is being extracted.'):
            index_webpage(page_url)

        st.success(f"Webpage extracted successfully.")
        time.sleep(2)
        st.rerun()
