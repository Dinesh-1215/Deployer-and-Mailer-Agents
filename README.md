Code Deployer & Mail Agent

A powerful Streamlit-based application that allows you to manage GitHub repositories, deploy code, and generate AI-powered job application emails using Gemma/Gemini models.

⸻

🚀 Features

🧰 Code Deployer
	•	Upload multiple files or a zipped folder.
	•	Automatically generate a README.md file.
	•	Push the uploaded content to a GitHub repository.
	•	Manage existing repositories (list & delete).

💼 Job Email Generator
	•	Upload a PDF/DOCX resume or paste your resume text.
	•	Sanitize personal data (email, phone numbers).
	•	Paste or upload a Job Description (JD).
	•	Generate a professional email using Gemma.
	•	Edit, review, and send the generated email via Gmail.
	•	Log all sent emails in a local folder.

⸻

🧱 Project Structure

codepush-agent/
├── app.py                # Main Streamlit application
├── github_agent.py       # Handles GitHub operations
├── gemma_agent.py        # Generates email content via Gemma
├── gmail_sender.py       # Sends emails via Gmail
├── requirements.txt      # Dependencies (recommended)
├── .env                  # Environment variables (ignored in Git)
└── README.md             # This file


⸻

⚙️ Installation

1. Clone the repository

git clone https://github.com/<your-username>/codepush-agent.git
cd codepush-agent

2. Create a virtual environment

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root:

GITHUB_TOKEN=ghp_xxx...         # Your GitHub personal access token
GMAIL_ADDRESS=you@example.com    # Default sender email
APP_LOG_DIR=logs                 # Optional custom log folder
GEMINI_API_KEY=AIza...           # Optional Gemini key

⚠️ Never push .env or token files to GitHub.

⸻

🧩 Usage

Run the app locally:

streamlit run app.py

Then open the displayed URL, usually http://localhost:8501￼

🔹 Tab 1: Code Deployer
	1.	Enter GitHub repo name, branch, and commit message.
	2.	Upload files or a zipped project folder.
	3.	Optionally auto-generate a README.md.
	4.	Click Push to GitHub.
	5.	View upload status and logs.

🔹 Tab 2: Job Email Generator
	1.	Paste or upload your resume.
	2.	Paste the job description.
	3.	Click Generate Email (Gemma-powered).
	4.	Edit and review the AI-generated email.
	5.	Enter recipient and your Gmail, then send.
	6.	A copy of each sent email is saved in the logs/ folder.

⸻

🪄 Requirements

Python >= 3.10

Example requirements.txt:

streamlit
PyMuPDF
python-docx
python-dotenv
requests
gitpython
scikit-learn
numpy
google-genai  # optional

Install all:

pip install -r requirements.txt


⸻

🧰 Security & Git Hygiene

Create a .gitignore file with:

# Secrets
.env
token.json
token.pickle
credentials.json

# Virtual environments
venv/
.venv/

# Logs
logs/
*.log

# Cache
__pycache__/
.streamlit/

Remove tracked secret files

git rm --cached .env token.json token.pickle credentials.json

Then commit & push safely:

git add .gitignore
git commit -m "Remove sensitive files and add .gitignore"
git push origin main

If GitHub blocks your push due to secrets, purge them with:

pip install git-filter-repo
git filter-repo --path .env --path token.json --path token.pickle --path credentials.json --invert-paths
git push origin --force


⸻

🐳 Optional: Run in Docker

Dockerfile:

FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]

Build & run:

docker build -t codepush-agent .
docker run -p 8501:8501 --env-file .env codepush-agent


⸻

🧾 Example Log Output

✅ Email sent and saved to logs!
[LOG] 2025-11-09 16:12:23 - push_folder_to_github: success
[LOG] 2025-11-09 16:13:01 - resume extraction successful


⸻

👨‍💻 Author

Dinesh Karri
AI & ML Engineer | TCS Bangalore
GitHub Profile￼

⸻

🪶 License

MIT License © 2025 Dinesh Karri

⸻

⚡ Code smarter. Apply faster. — Automate your Git pushes and job emails with AI.
