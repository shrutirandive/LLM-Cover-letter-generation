import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from datetime import datetime
import pydoc
from dotenv import load_dotenv
import PyPDF2 as pdf
import re
# from transformers import pipeline

load_dotenv()

# Get current date
c_date = datetime.now()
# Format the date as 'Month Day, Year'
current_date = c_date.strftime("%B %d, %Y")
print(current_date)

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def input_pdf_text(uploaded_file):
        reader=pdf.PdfReader(uploaded_file)
        pdf_text=""
        for page in range(len(reader.pages)):
            page=reader.pages[page]
            pdf_text+=str(page.extract_text())
        return pdf_text

    def extract_data_from_pdf(self, pdf_text):
        pdf_prompt = PromptTemplate.from_template(f"""
        Your job is to Extract the following details from the resume text below and return them in JSON format containing the 
            following keys:
        - Full Name
        - Degree
        - University
        - Years of Experience
        - Work Experience
        - Skills
        - Projects
        - Contact Number
        - Email

        Resume Text: 
        {pdf_text}
        ### VALID JSON (NO PREAMBLE):

        """)

        # Generate output from the model
        chain_extract_pdf = pdf_prompt | self.llm 
        pdf_resp = chain_extract_pdf.invoke(input={"page_data": pdf_text})
        try:
            json_parser = JsonOutputParser()
            pdf_resp = json_parser.parse(pdf_resp.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        # print("==== Resume =====")
        # print (pdf_resp)
        return pdf_resp 


    def extract_data(self, cleaned_text):
        # creating prompt to extract data i.e. roles, experience, skills, etc from the scrapped data
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE OR GIVEN JOB DESCRIPTION:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website. OR there is a text having job description
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: 'company_name', 'company_address', 'role', 'experience', 'skills', 'description' and 'about'.
            elaborate all 'experience' in 2nd paragraph.
            
            Experience or Qualifications are same and would stored in 'experience'.            
            Skills, or Technology or Abilities would be stored in 'skills'.            
            Fetch job details from the description, names having engineer, Analyst, developer, business, cloud and store in 'role'.
            In 'about' include description about company mentioned in the website about the company_name.
            In 'company_address' include any of the company Locations mentioned in website. 
            
            
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):    
            """
        )
        # using pipe operation - to create a chain from getting a prompt and passing it to llm
        chain_extract = prompt_extract | self.llm 
        resp = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            resp = json_parser.parse(resp.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        # print("==== Job Description =====")
        # print(resp)
        return resp if isinstance(resp, list) else [resp]
    
    def write_cover_letter(self, company_name, description, company_address, about, role, skills, experience, 
                           full_name, contact_number, email, degree, resume_skills, resume_experience):
        prompt_cover_letter = PromptTemplate.from_template(
            """ 
            ### INSTRUCTION:
            Elborate these keys in cover letter, do not include all mention few of them matching job description 'resume_skills', 'resume_experience'. 
            Pick one experience each and mention that in my cover letter into grammatical correct sentence.
            Include in pragraph to show interest about the company and include few lines from 'about' in last paragraph.
            Also make only 3 paragraphs for the cover letter.

            ###COVER LETTER
            {current_date}

            Hiring Manager,  
            Human Relations Department,  
            {company_name},  
            {company_address}

            Dear Hiring Manager,

            I am excited to apply for the {role} position at {company_name}. 
            With a {degree}, I have developed a robust foundation in {resume_skills}. My experience as a {resume_experience} have sharpened my skills in designing, developing, and deploying scalable data solutions.           
            In my previous roles, {resume_experience}
            I am enthusiastic about the opportunity to contribute to {company_name}'s and {about} innovative goals and would welcome the chance to discuss how my skills align with your team's needs. 
            I look forward to the possibility of discussing my experience and qualifications further for the {role} position at {company_name}. 
            Please feel free to contact me at {contact_number} or {email}. Thank you very much for your time and consideration.
            Please find my resume attached for your review.
            
            Sincerely,  
            {full_name}
            Do not provide a preamble.           
            """
        )
        chain_cover_letter = prompt_cover_letter | self.llm

        # Example of how to invoke it without links
        res = chain_cover_letter.invoke({
                    "company_name": str(company_name),
                    "job_description": str(description), 
                    "company_address": str(company_address), 
                    "about": str(about),
                    "role": str(role), 
                    "skills": str(skills),    
                    "experience": str(experience),    
                    "current_date": str(current_date),
                    "full_name" : str(full_name),
                    "contact_number" : str(contact_number),
                    "email" : str(email),
                    "degree" : str(degree),
                    "resume_experience" : str(resume_experience),
                    "resume_skills" : str(resume_skills),
                })

        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
