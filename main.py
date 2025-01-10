import streamlit as st
from io import StringIO
from PyPDF2 import PdfReader
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import FireCrawlLoader

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key not found. Please set it in the .env file.")
    st.stop()
client = OpenAI(api_key=api_key)

# Define functions for crawling and analysis
def analyze_job_requirements(job_url):
    try:
        # Get the API key from environment variables
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set FIRECRAWL_API_KEY in your environment.")

        # Initialize FireCrawlLoader for the job URL
        loader = FireCrawlLoader(
            url=job_url,
            api_key=api_key,
            mode="scrape",  # Use "scrape" for single page extraction
        )

        # Load the document
        documents = loader.load()

        # Extract content from the document
        if documents:
            job_description = documents[0].page_content

            # Debug: Print the first 500 characters of the extracted content
            print("Extracted text (first 500 characters):")
            print(job_description[:500])  # Show only the first 500 characters for brevity

            return job_description
        else:
            print("No content extracted.")
            return None

    except Exception as e:
        # Print the error for debugging
        print(f"An error occurred while fetching the job description: {e}")
        return None

def analyze_resume(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)
    elif uploaded_file.type in ["text/plain", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        text = uploaded_file.read().decode("utf-8")
    else:
        return "Unsupported file format. Please upload a PDF, TXT, or Word file."

    return text

def generate_customized_documents(job_analysis, resume_analysis):
    # Generate customized resume
    resume_prompt = (
        f"Based on the job analysis: {job_analysis},\n"
        f"and resume analysis: {resume_analysis},\n"
        f"I am re-writing my resume and I need your help. You are going to act as a professional resume writer skilled in presenting information concisely and using niche-appropriate language, while avoiding redundancy and cliché terms. Your task is to position my experience as a solution to my target companys pain points, tailoring it specifically so that its clear that I can manage the primary requirements of the job. I want you to memorize these instructions for the duration of our session. generate a customized resume for this job, make it sounds like I am the perfect match. Format it professionally."
    )
    resume_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Generate tailored resumes, make it sounds like I'm the perfect match."},
            {"role": "user", "content": resume_prompt}
        ]
    )
    customized_resume = resume_response.choices[0].message.content

    # Generate customized cover letter
    cover_letter_prompt = (
        f"Based on the job analysis: {job_analysis},\n"
        f"and resume analysis: {resume_analysis},\n"
        f"generate a customized cover letter for this job. Include my personal information. Format it professionally and ready to send."
    )
    cover_letter_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Generate tailored cover letters. Make it sounds like I am the perfect match, and pleade make it sound positive"},
            {"role": "user", "content": cover_letter_prompt}
        ]
    )
    customized_cover_letter = cover_letter_response.choices[0].message.content

    return customized_resume, customized_cover_letter

import streamlit as st

# Streamlit app
st.title("Customized Resume and Cover Letter Generator")

# Step 1: Input Job Description
st.header("Step 1: Input Job Description")
job_url = st.text_input("Enter the URL of the job posting (optional):", key="job_url_input")

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if st.button("Extract Job Description", key="extract_button"):
    if job_url:
        with st.spinner("Extracting job description..."):
            job_description = analyze_job_requirements(job_url)
            if job_description:
                st.session_state.job_description = job_description
                st.success("Job description extracted successfully!")
            else:
                st.warning("Failed to extract job description. Please input it manually below.")
    else:
        st.warning("Please enter a job URL to extract the job description or proceed with manual input.")

# Display a textarea for manual job description input or edits
job_description_input = st.text_area(
    "Job Description (Auto-Extracted or Enter Manually):",
    st.session_state.job_description,
    placeholder="Enter or edit the job description here if extraction fails or no URL is provided.",
    height=300,
    key="job_description_input"
)
st.session_state.job_description = job_description_input

# Step 2: Upload Resume
st.header("Step 2: Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (PDF, TXT, Word):", type=["pdf", "txt", "doc", "docx"], key="resume_file_uploader")

if "customized_resume" not in st.session_state:
    st.session_state.customized_resume = None

if "customized_cover_letter" not in st.session_state:
    st.session_state.customized_cover_letter = None

# Generate documents button
if st.button("Generate Documents", key="generate_button"):
    if st.session_state.job_description and resume_file:
        with st.spinner("Analyzing inputs and generating documents..."):
            resume_analysis = analyze_resume(resume_file)
            customized_resume, customized_cover_letter = generate_customized_documents(
                st.session_state.job_description, resume_analysis
            )
            st.session_state.customized_resume = customized_resume
            st.session_state.customized_cover_letter = customized_cover_letter
        st.success("Documents generated successfully!")
    else:
        st.warning("Please provide both the job description and resume to generate documents.")

# Step 3: Download Documents
st.header("Step 3: Download Your Customized Documents")

if st.session_state.customized_resume and st.session_state.customized_cover_letter:
    st.download_button(
        label="Download Customized Resume",
        data=st.session_state.customized_resume,
        file_name="customized_resume.txt",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    st.download_button(
        label="Download Customized Cover Letter",
        data=st.session_state.customized_cover_letter,
        file_name="customized_cover_letter.txt",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
else:
    st.info("Customized documents will appear here for download once generated.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: small; color: grey;">
        Contact me at: <a href="mailto:situjx@hotmail.com">situjx@hotmail.com</a> <br>
        <i>We do not store or use your personal data.</i>
    </div>
    """,
    unsafe_allow_html=True
)