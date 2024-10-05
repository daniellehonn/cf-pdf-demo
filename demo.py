import streamlit as st
from model_hub.config import PRICING
from model_hub.controller import ask_llm
from utils.vectorization import vector_similarity_search, pinecone_remove_all
from utils.navigation import make_sidebar

# Function to generate response using LLM based on context
def generate_llm_response(context, query, selected_model):
    return ask_llm(data={"context": context,"query": query}, selected_model=selected_model)


st.title("ContextForce PDF Parser Demo 🍓")
make_sidebar()

model_selection = st.session_state.get("model_selection")

query = st.text_input("Enter your query:")

if st.button("Ask", type="primary"):
    sources = ''
    with st.spinner("Searching for relevant context..."):
        # Search Pinecone for relevant context
        search_results = vector_similarity_search(query)
        context = ''
        for idx, res in enumerate(search_results, start=1):  # start=1 to start numbering from 1
            context += f"\n[SOURCE #{idx}]\n"
            context += f"Name: {res.metadata.get('source_name')}\n"  
            context += f"Source: {res.metadata.get('source')}\n"  # Using 'source' as URL or pdf name
            context += f"Content #{idx}:\n"
            context += f"{res.page_content}\n"
            sources += (f"[SOURCE #{idx}]: [{res.metadata.get('source_name')}]({res.metadata.get('source')})  \n")

        print(context, sources)
    
    # Generate response using LLM based on the context
    with st.chat_message("user"):
        st.write(f"{query}")
    with st.spinner("Generating response using LLM..."):
        response = generate_llm_response(context, query, selected_model=model_selection)
        with st.chat_message("assistant"):
            st.write(f"{response}")
            st.markdown(f"**Context Sources**  \n{sources}")

    

st.markdown("---")
st.write("Powered by [ContextForce](https://contextforce.com/)")
if st.button("Delete All Vectors"):
    pinecone_remove_all()



