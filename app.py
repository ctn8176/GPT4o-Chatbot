import streamlit as st
from emailGen import generate_email
from chatbot import generate_chatbot
import toml

secrets = toml.load(".streamlit/secrets.toml")
api_key = st.secrets["OPENAI_API_KEY"]


def main():
    st.set_page_config(page_title="Chatbot (GPT-4o)", page_icon=":rocket:")

    # Display the select box in the sidebar
    option = st.sidebar.selectbox("Select an option:", ["Generate Email", "Chat with Multimodal Chatbot"], index=0)

    if option == "Generate Email":
        generate_email()
    elif option == "Chat with Multimodal Chatbot":
        generate_chatbot()

if __name__ == '__main__':
    main()