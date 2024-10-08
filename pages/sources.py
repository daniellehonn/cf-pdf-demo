import streamlit as st
import time
from utils.d1 import delete_source, get_sources
from utils.navigation import make_sidebar
from io import BytesIO

from utils.r2_upload import delete_file_from_r2
from utils.vectorization import pinecone_remove_all, pinecone_remove_source

st.title("Sources")
make_sidebar()

svg_map = {
    "pdf": "https://www.svgrepo.com/show/484113/pdf-file.svg",
    "youtube": "https://www.svgrepo.com/show/13671/youtube.svg",
    "webpage": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcT3z6OLss2pupQutUN28SqSx2KvP8Uq-HNWMZly_AxxcuZf6TPk",
}

sources = get_sources()

for item in sources:
    col0, col1, col2 = st.columns([1, 9, 1])  # Create two columns for layout
    with col0:
        if item["Type"] == 'youtube':
            try:
                st.image(item["Thumbnail_Url"], use_column_width='auto')
            except:
                st.image(svg_map[item["Type"]], use_column_width='always')
        else:
            st.image(svg_map[item["Type"]], use_column_width='always')  # Display the icon
    with col1:
        with st.expander(item["Name"]):  # Create an expander for each item
            # Display the nested information
            if item['Type'] != 'youtube':
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
            pinecone_remove_source(item['Name'])
            st.rerun()

st.markdown("---")
if st.button("Wipeout All Source Vectors"):
    pinecone_remove_all()
