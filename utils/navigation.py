import streamlit as st
from model_hub.config import PRICING

def make_sidebar():
    with st.sidebar:
        st.title("Web Scraper Settings")
        st.session_state.model_selection = st.sidebar.selectbox("Select Model", options=list(PRICING.keys()), index=0)

