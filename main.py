import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from utils import clean_text
import pandas

def create_streamlit_app(llm, clean_text):
    st.title(":page_with_curl: Build your Cover Letter")
    with st.sidebar:        
        url_input = st.text_input("Enter a URL:")
        st.markdown("OR")
        job_descrip = st.text_area("Paste Job description")
        print(job_descrip)
        st.divider()
        uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")
    
        submit_button = st.button("Submit")

    if submit_button:
         # Check if either URL or Job Description is provided (not both)
        if (url_input and job_descrip) or (not url_input and not job_descrip):
            st.error("Please provide either a URL or a Job Description, but not both.")
            return

        # Check if the resume file is uploaded
        if uploaded_file is None:
            st.error("Please upload your resume in PDF format.")
            return
        try:
            # getting data from the uploaded resume PDF
            pdf_text = Chain.input_pdf_text(uploaded_file)
            # extracting data from pdf text to keys
            resume = llm.extract_data_from_pdf(pdf_text)
            # print(resume, type(resume))
            
            full_name = resume.get('Full Name')
            contact_number = resume.get('Contact Number')
            email = resume.get('Email')
            degree = resume.get('Degree')
            resume_skills = resume.get('Skills')
            resume_experience = resume.get('Work Experience')
            
            # If a URL is provided, scrape job description from URL
            if url_input:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                # Extract job data from URL
                jobs = llm.extract_data(data)
            # If a job description is provided, use it directly
            elif job_descrip:
                data = clean_text(job_descrip)
                jobs = llm.extract_data(data)
            # print("========================")
            # print(jobs)
            for job in jobs:
                company_name = job.get('company_name',[])
                description = job.get('description',[])
                company_address = job.get('company_address',[])
                about = job.get('about',[])
                role = job.get('role',[])
                experience = job.get('experience',[])
                skills = job.get('skills', [])

            letter = llm.write_cover_letter(company_name, description, company_address, about, role, skills, experience, 
                                            full_name, contact_number, email, degree, resume_skills, resume_experience)
                # st.code(letter, language='markdown')
            st.markdown('')
            st.markdown(":red[(Revise your cover letter accordingly!!)]")
            st.markdown(letter)
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cover Letter Generator", page_icon="📧")
    create_streamlit_app(chain, clean_text)
