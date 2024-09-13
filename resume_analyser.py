import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from streamlit_player import st_player

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt=""""Assume the role of a seasoned ATS (Application Tracking System) expert with in-depth knowledge of the tech industry, software engineering, data science, data analysis, and big data engineering. Your mission is to meticulously evaluate the provided resume against the given job description, considering the highly competitive job market.
Provide a comprehensive analysis in the following format:
Resume Evaluation Report
Job Description Match: % (assign a percentage score based on how well the resume aligns with the job description)
Missing Keywords: [] (list the essential keywords and phrases from the job description that are absent or underemphasized in the resume)
Profile Summary: (offer a concise, actionable summary of the candidate's strengths and weaknesses, highlighting areas for improvement)
Job Suitability: (provide a clear, definitive answer: 'Yes, the candidate is suitable for the job' or 'No, the candidate is not suitable for the job')
Additional Recommendations: (optional, but highly valuable: provide specific, constructive suggestions for improving the resume, including tips for enhancing relevant skills, experience, and keywords)
Please analyze the resume and job description with utmost care, ensuring your response is accurate, informative, and helpful for the candidate."
"""

## streamlit app setup
st.set_page_config(page_title='Resume Analyzer',
                   layout='wide',
                   )
st.sidebar.title(" Smart ATS Resume Analyzer ")
# with st.sidebar.container(): 
#     st.image('', use_column_width=True, caption='Resume analzer')
st.sidebar.markdown("---")

def print_praise():
    praise_quotes = """
    Varun Gupta
    """
    title = "**Created By -**\n\n"
    return title + praise_quotes

st.sidebar.info(print_praise())   
st.sidebar.write("---\n")
st.sidebar.title(" History ")
st.sidebar.write("---\n")



# st.sidebar.write("This is a simple text without formatting.")
# st.sidebar.markdown("This is **bold** and _italic_ text using Markdown.")
name=st.text_input("what is your name ?")
jd=st.text_area("Write Job Description Here ")
uploaded_file=st.file_uploader("Upload Resume",type="pdf",help="Please Uplaod PDF ")

submit = st.button("Submit")
st.write("\n\n"*4)


if "history" not in st.session_state:
    st.session_state.history = []

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        
        prompt = f"Analyze the following resume: {text}\nJob Description: {input_prompt}"
        
        response=get_gemini_repsonse(prompt)

        st.subheader(response)
        
        prompt = f"Analyze the following resume: {text}\nJob Description:{jd} and only tell me that the candidate  is eligible for the job or not "

        response2=get_gemini_repsonse(prompt)

        st.session_state.history.append({"job disc": jd, "job_suitability": response2,"name":name})
    


    for chat in st.session_state.history:
        st.sidebar.markdown(f"Name :{chat['name']}")


        st.sidebar.markdown(f"Job Discription :{chat['job disc']}")


        st.sidebar.markdown(f"job_suitability :{chat['job_suitability']}")


st.success("See The Video To Make Resume in case if you dont have   .\n\n")
youtube_url = "https://youtu.be/KZehm-meGMg?si=MrFZzKkyY6yGm90r"
st_player(youtube_url)