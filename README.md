# resumebuilder

Customized Resume and Cover Letter Generator

This project is a Streamlit-based application designed to help users generate tailored resumes and cover letters for specific job postings. It uses OpenAI's GPT-4 API for text generation and leverages web scraping tools to analyze job descriptions.

Features

Input a job posting URL to extract job requirements.

Upload a resume (PDF, TXT, DOC, or DOCX) for analysis.

Generate a professionally formatted resume and cover letter customized to the job.

Download the generated documents directly from the app.

Prerequisites

Python 3.8+

An OpenAI API key

Installation

Clone the repository:

git clone <repository-url>
cd <repository-directory>

Set up a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Create a .env file in the project directory:

OPENAI_API_KEY=your_openai_api_key_here

Exclude sensitive files from version control by adding the following to .gitignore:

.env

Running the Application

Start the Streamlit app:

streamlit run app.py

Open the app in your browser using the URL provided by Streamlit (usually http://localhost:8501).

Usage

Enter the job posting URL in the provided text box.

Upload your resume in a supported format.

Click the "Generate Documents" button to create a customized resume and cover letter.

Download the generated documents using the provided download buttons.

File Structure

app.py: Main application script.

requirements.txt: List of required Python libraries.

.env: Environment variables file (not included in version control).

Dependencies

streamlit: For building the app interface.

requests: For HTTP requests to fetch job postings.

beautifulsoup4: For parsing HTML content.

PyPDF2: For extracting text from PDF files.

python-dotenv: For securely loading environment variables.

openai: For interacting with the OpenAI GPT-4 API.

Security Considerations

API Key Management: Store your OpenAI API key securely in the .env file. Do not hardcode it in the source code.

HTTPS: Use HTTPS if deploying to a production environment to secure data transmission.

Deployment

You can deploy this application using platforms like:

Streamlit Cloud

AWS

Google Cloud

Heroku

Contributing

Feel free to submit issues or pull requests to improve the project.

License

This project is licensed under the MIT License. See the LICENSE file for details.