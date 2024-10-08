import streamlit as st
from model_hub.config import PRICING
from utils.d1 import get_sources, delete_source
from utils.r2_upload import delete_file_from_r2
from utils.vectorization import pinecone_remove_source
import pandas as pd

def make_sidebar():
    with st.sidebar:
        st.title("Web Scraper Settings")
        st.session_state.model_selection = st.sidebar.selectbox("Select Model", options=list(PRICING.keys()), index=0)




