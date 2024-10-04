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

        st.markdown("---")
        st.title("Sources")


        sources = get_sources()
        # Convert to DataFrame
        # df = pd.DataFrame(sources)

        # st.data_editor(df, key="edited_data", num_rows="dynamic")
        # if st.session_state["edited_data"]['deleted_rows']:
        #     for i in st.session_state["edited_data"]['deleted_rows']:
        #         delete_source(i+1)


        for item in sources:
            col1, col2 = st.columns([9, 1])  # Create two columns for layout
            with col1:
                with st.expander(item["Name"]):  # Create an expander for each item
                    # Display the nested information
                    st.markdown(f"**MD URL:** [{item['MD_file']}]({item['MD_file']})")
                    st.markdown(f"**Source URL:** [{item['Source']}]({item['Source']})")
                    st.markdown(f"**# of Vectors:** {item['Num_Vectors']}")
            with col2:
                # Create a delete button for each item
                if st.button("🗑️", key=item["SourceID"]):  # Delete icon button
                    # Remove from D1
                    delete_source(item['SourceID'])

                    # Remove from R2
                    delete_file_from_r2(item['MD_file'].replace('https://r2.contextforce.com/', ''))
                    if item['Type'] == 'pdf':
                        delete_file_from_r2(item['Source'].replace('https://r2.contextforce.com/', ''))
                    
                    # Remove from Vectorstore
                    pinecone_remove_source(item['Source'])
                    st.rerun()


