import streamlit as st
import pandas as pd 
from PyPDF2 import PdfReader
import toml
from openai import OpenAI

client = OpenAI()

secrets = toml.load(".streamlit/secrets.toml") 

# Accessing the OpenAI API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Setting up the OpenAI API client

def generate_chatbot():
    st.title("Multimodal Chatbot (GPT-4o)")
    st.markdown("Analyze a PDF or CSV file, powered by OpenAI's newly released model (GPT-4o).")


    # Sidebar for file upload
    uploaded_file = st.sidebar.file_uploader("Upload a PDF or CSV file", type=["pdf", "csv"])

    # Initialize variable to store uploaded file content
    uploaded_file_content = None

    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            # Read PDF file
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            st.sidebar.text("PDF content:")
            st.sidebar.text(text)
            uploaded_file_content = text
        elif uploaded_file.type == "text/csv":
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            st.sidebar.text("CSV file content:")
            st.sidebar.write(df)
            uploaded_file_content = df.to_dict()

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("How can I help you today? :)")
    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Append uploaded file content to messages if available
            if uploaded_file_content:
                st.session_state["messages"].append({"role": "user", "content": uploaded_file_content})

            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state["messages"]
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state["messages"].append({"role": "assistant", "content": response})
