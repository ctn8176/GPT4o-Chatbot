import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

client = OpenAI() 
import toml

secrets = toml.load(".streamlit/secrets.toml")

def generate_email():
    st.title("Personalized Email Generator (GPT-4o)")
    st.markdown("Enter a link to web scrape and generate a personalized email powered by OpenAI's newly released model (GPT-4o). Happy emailing! 👩‍💻")

    # Input field for website link
    website_link = st.text_input("Enter the website link:")

    # Handle form submission
    if st.button("Generate Email"):
        # Check if website link is provided
        if website_link:
            try:
                # Scrape the website content
                response = requests.get(website_link)
                response.raise_for_status()  
                soup = BeautifulSoup(response.text, "html.parser")
                company_data = " ".join([p.text for p in soup.find_all("p")])

                # Generate personalized email using GPT-4o
                with st.spinner("Generating Email..."):
                    completion = client.chat.completions.create(model="gpt-4o",
                    messages=[
                        {"role": "system", "content": f"You are a helpful sales assistant writing to {company_data}. Write a personalized email using the {company_data} to sell a product."},
                        {"role": "user", "content": "Hello!"}
                    ])
                email_content = completion.choices[0].message.content  
                st.subheader("Generated Email:")
                st.write(email_content)
            except requests.exceptions.RequestException as e:  # Added error handling
                st.error(f"An error occurred while fetching the website: {e}")
            except Exception as e:  
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a website link.")

# Call the function to display the Streamlit app
generate_email()
