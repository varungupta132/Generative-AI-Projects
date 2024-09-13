import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Set page config
st.set_page_config(
    page_title="Chat Using PDF With Varun",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load environment variables from .env file
load_dotenv()

# Get the value of GOOGLE_API_KEY from environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Display API key loading status in the app's interface
st.write("Made By Varun Gupta .......")
# if api_key:
#     st.write("API key found in .env file!")
#     st.write(f"API key: {api_key}")
#     genai.configure(api_key=api_key)
# else:
#     st.error("GOOGLE_API_KEY not found in .env file.")

# Rest of your code...
model = genai.GenerativeModel("gemini-pro")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        if pdf_reader.pages:  # Check if the list is not empty
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            print("Warning: PDF file is empty or doesn't have any pages.")
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def load_faiss_index(pickle_file):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    faiss_index = FAISS.load_local(pickle_file, allow_dangerous_deserialization=True, embeddings=embeddings)
    return faiss_index

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

prompt_template = """
Answer the questions in as much detail as possible based on the provided context. Ensure that your answers align with the given context. If the context is unclear or insufficient, do not provide incorrect or assumed answers. Instead, specify the exact information you need to answer the queries accurately. If necessary, respond with thanks.
Additionally, if definitions, key terms, or examples related to the context are requested, please provide them.
\n\n 
Context:\n{context}?\n
Question:\n{question}\n
Answer:
"""

def get_conversational_chain():
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embeddings-001")
    new_db = load_faiss_index("faiss_index")
    docs = new_db.similarity_search(user_question)
    if docs:  # Check if the list is not empty
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": user_question})
        st.write("**Reply:**", response["output_text"])
    else:
        st.write("No relevant documents found.")

def main():
    st.header("Chat with PDF ")
    st.write("First Uplode a PDF And Then Ask Me Questions Related To PDF")
    user_question = st.text_input("Ask a Question")
    if user_question:
        user_input(user_question)

    temperature = st.sidebar.slider("Temperature", min_value=0.1, max_value=1.0, step=0.1, value=0.3)
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your Files and Click Submit", accept_multiple_files=True, type=["pdf"])
        if st.button("Submit"):
            with st.spinner("Uploading..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.success("VectorDB Upload Finished")

if __name__ == "__main__":
    main()