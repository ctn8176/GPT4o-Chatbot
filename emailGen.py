import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import toml

secrets = toml.load(".streamlit/secrets.toml")
api_key = st.secrets["OPENAI_API_KEY"]

company_info = """
* Coast is a Visa fleet fuel and gas card plus expense management solution that helps fleets control and track employee spending on fuel and other expenses
* Our mission is to help businesses save time and money, so business owners can focus on what matters
* Fleet cards and spend management are a tool to help your business do that. Our easy-to-use software lets you set rules that work for your business and track fleet spending so you don’t miss a thing
* Get visibility on risky transactions so you can set rules and stop abuse and fraud before it can impact your business
* Your drivers can fuel up anywhere Visa can be used instead of searching for an “in-network” gas station. And we offer simple, low pricing that’s easy to understand, plus 2¢ off per gallon on your statement
"""

def generate_email():
    st.title("Personalized Email Generator (GPT-4o)")
    st.markdown("Enter a link to web scrape and generate a personalized email powered by OpenAI's newly released model (GPT-4o). Happy emailing! 👩‍💻")

    # Input field for website link
    with st.form("website_form"):
        website_link = st.text_input("Enter the website link:")
        submitted = st.form_submit_button("Generate Email")

    # Handle form submission
    if submitted:
        # Check if website link is provided
        if website_link:
            try:
                # Scrape the website content
                response = requests.get(website_link)
                response.raise_for_status()  
                soup = BeautifulSoup(response.text, "html.parser")
                prospect = " ".join([p.text for p in soup.find_all("p")])

                # Generate personalized email using GPT-4o
                with st.spinner("Generating Email..."):
                    completion = openai.chat.completions.create(model="gpt-4o",
                    messages=[
                        {"role": "system", 
                         "content": 
                             f"""You work for {company_info}. You are an SDR and you are to write a personalized sales outbound email to {prospect} using the {prospect} information that the user uploaded.
                             Be sure to use value selling: A sales methodology that focuses on how your product or service will provide value to the customer instead of focusing on price or solution.
                             Keep the email short - under 1000 characters"""},
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

if __name__ == '__main__':
    generate_email()
