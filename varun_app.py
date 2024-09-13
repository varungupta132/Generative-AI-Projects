
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel()


def get_resposne(question):
    response = model.generate_content(question)
    return response.text 


st.set_page_config(
    page_title="Chatbot Interface",
    layout="wide",
    initial_sidebar_state="expanded"
    )

st.sidebar.header("Chat History")
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for chat in st.session_state.history:
    st.sidebar.markdown(f"{chat['question']}")
    st.sidebar.markdown(f"{chat['response']}")


#When submit is clkicked

# Main interface
st.title("GemChatbot")
st.text("Powered By Varun Gupta")
question = st.text_input("Ask any question:")

if st.button("Submit"):
    if question:
        response = get_resposne(question)
        st.session_state.history.append({"question": question, "response": response})
        st.write("*You:*", question)
        st.write("*Answer:*", response)

# Save the updated chat history
st.session_state.history = st.session_state.history





































































# if submit:
#     response = get_gemini_resposne(input)
#     st.write(response)

# st.header("QUestion Answers by gemini")
# input= st.text_input("Input:",key="input")
# submit = st.button("Ask your Questions")

# Sidebar for chat history             you have to creat code according to this and have to use these libraries as requied