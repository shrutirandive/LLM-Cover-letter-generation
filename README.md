# Cover Letter Generation
This project helps users create tailored cover letters for specific job postings. The application accepts either a job description (provided through a URL or pasted directly), alongside the user's resume in PDF format. Using an LLM (Large Language Model), the application extracts relevant details from both the job description and the resume to generate a customized cover letter.

## Tools & Technologies Used
**Streamlit**: Used to build the front-end interface.

**Langchain Community & Core**: Provides document loading, prompt templates, and output parsing.

Instead of installing and using LLaMA locally, we will be using Groq, as it takes a lot of time to run. Groq is a platform that allows you to run LLaMA 3.1 in the cloud. The inference is very fast because they use LPU

**Groq LLaMA**: A large language model used for generating content and extracting data.

**PyPDF2**: For extracting text from PDF files.

**Python**: The primary programming language used in this project.

## Setup

1. Clone the repository

2. Install dependencies
```pip install -r requirements.txt```

3. Set Up Environment Variables: Create a .env file in the root directory and add your API keys 
```GROQ_API_KEY=your_groq_api_key_here```

4. Run the Application ```streamlit run main.py```

