# Smart Resume Screener 🚀

An AI-powered Resume Screening and Candidate Shortlisting System built using Flask, Google Gemini AI, and Twilio.

This application helps recruiters automatically analyze resumes, match them with job descriptions, rank candidates, and send notifications via Email and WhatsApp.

------------------------------------------------------------
FEATURES
------------------------------------------------------------

- Upload multiple resumes (PDF, DOCX, TXT)
- AI-powered resume analysis using Gemini API
- Resume scoring and ranking
- Skill matching with Job Description
- Category-based filtering
- Send Emails to shortlisted candidates
- WhatsApp notifications using Twilio
- Download shortlisted candidates as CSV
- Automatic project report PDF generation

------------------------------------------------------------
TECH STACK
------------------------------------------------------------

Backend:
- Python
- Flask

AI Model:
- Google Gemini API

Communication:
- SMTP Email
- Twilio WhatsApp API

Frontend:
- HTML
- CSS
- Bootstrap

File Processing:
- PyPDF2
- python-docx

Deployment:
- Gunicorn

------------------------------------------------------------
PROJECT STRUCTURE
------------------------------------------------------------

Smart-Resume-Screener/
│
├── app.py
├── generate_paper.py
├── requirements.txt
├── .gitignore
│
├── uploads/
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   ├── dashboard.html
│   ├── sorted_resumes.html
│   └── message_sent.html
│
├── utils/
│   ├── extract_text.py
│   └── scoring.py
│
└── static/

------------------------------------------------------------
INSTALLATION & SETUP
------------------------------------------------------------

1. Clone the Repository

git clone https://github.com/your-username/smart-resume-screener.git
cd smart-resume-screener

------------------------------------------------------------

2. Create Virtual Environment

Windows:
python -m venv venv
venv\Scripts\activate

Linux / Mac:
python3 -m venv venv
source venv/bin/activate

------------------------------------------------------------

3. Install Dependencies

pip install -r requirements.txt

------------------------------------------------------------
ENVIRONMENT VARIABLES
------------------------------------------------------------

Create a .env file in the root directory.

GEMINI_API_KEY=your_gemini_api_key

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password

TWILIO_SID=your_twilio_sid
TWILIO_AUTH=your_twilio_auth_token
TWILIO_NUMBER=whatsapp:+14155238886

------------------------------------------------------------
HOW TO RUN THE PROJECT
------------------------------------------------------------

Run the Flask application:

python app.py

Server will start at:

http://127.0.0.1:5000/

Open the URL in your browser.

------------------------------------------------------------
HOW TO GENERATE PROJECT REPORT PDF
------------------------------------------------------------

Run:

python generate_paper.py

Generated PDF will be available inside:

uploads/Final_Report.pdf

------------------------------------------------------------
RESUME SCREENING WORKFLOW
------------------------------------------------------------

1. Upload resumes
2. Enter Job Description
3. Enter required skills
4. AI analyzes resumes
5. Candidates get ranked
6. Filter shortlisted candidates
7. Send notifications via Email/WhatsApp
8. Download shortlist CSV

------------------------------------------------------------
SUPPORTED RESUME FORMATS
------------------------------------------------------------

- PDF
- DOCX
- TXT

------------------------------------------------------------
AI SCORING LOGIC
------------------------------------------------------------

The system evaluates resumes based on:

- Job Description similarity
- Required skill matching
- Semantic understanding using Gemini AI
- Category detection

------------------------------------------------------------
FUTURE ENHANCEMENTS
------------------------------------------------------------

- Multi-language resume support
- AI interview scheduling
- Bias detection system
- Voice screening integration
- Cloud deployment

------------------------------------------------------------
AUTHOR
------------------------------------------------------------

Nandan K.P

------------------------------------------------------------
LICENSE
------------------------------------------------------------

This project is licensed under the MIT License.

------------------------------------------------------------
GITHUB UPLOAD STEPS
------------------------------------------------------------

Initialize Git:
git init

Add Files:
git add .

Commit:
git commit -m "Initial Commit"

Connect GitHub Repo:
git remote add origin https://github.com/your-username/repository-name.git

Push Code:
git branch -M main
git push -u origin main

------------------------------------------------------------
