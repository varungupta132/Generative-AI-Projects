import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Set up the Streamlit page
st.set_page_config(
    page_title="Marketing Copy Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("MarketMax Analyzer")


def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text




# Input boxes for product details and content type


product_details = st.text_input("Product Details:")

content_type_options = ["Product Description", "Advertisement", "Social Media Post", "Blog Post"]
content_type = st.selectbox("Content Type:", content_type_options)

role_description = """
You are a highly advanced product analyst AI with expertise in evaluating technology products across various domains.
Your goal is to provide a comprehensive and insightful analysis of any product details and content you are given, helping users make informed decisions.
"""


prompt = f"""
As an expert product analyst with a deep understanding of the tech industry, your task is to conduct a detailed analysis of the following product details: {product_details}. 
Your analysis should be informed by the content type: {content_type} and guided by your role as defined: {role_description}.

Please ensure your evaluation covers the following aspects:

1. **Product Overview**: Provide a clear and engaging description of what the product is, including its purpose and target audience.
2. **Compliments on Features**: Highlight the most impressive and standout features of the product, emphasizing what makes it special.
3. **Usefulness**: Explain how the product is beneficial for its users and why it would be valuable for them.
4. **Sales Strategy**: Offer strategies on how to effectively sell this product, including potential sales channels and marketing approaches.
5. **Growth Potential**: Provide insights into how the product's sales can be increased, including suggestions for expanding its market reach and improving customer engagement.

Your analysis should be thorough, persuasive, and tailored to help maximize the product's success in the market.
"""


submit = st.button("Generate Marketing Copy")

st.text("Powered By Your Company")

if submit:
        # Generate marketing copy based on product details and content type
                 
        response=get_gemini_repsonse(prompt)

        st.subheader(response)
        
        prompt = f"Analyze the following product detaiuls : {product_details} \n and the content type :{content_type} and tell me how i can grow the sells of this product and earn money write a big heading HOW TO SELL and tell every thing inside it  "

        # response2=get_gemini_repsonse(prompt)

        # st.subheader(response)

