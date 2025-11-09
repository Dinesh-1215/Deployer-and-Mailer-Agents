# Code Deployer & Mail Agent

A powerful **Streamlit-based application** that allows you to manage GitHub repositories, deploy code, and generate AI-powered job application emails using Gemma/Gemini models.

---

## 🚀 Features

### 🧰 Code Deployer
- Upload multiple files or a zipped folder.
- Automatically generate a `README.md` file.
- Push the uploaded content to a GitHub repository.
- Manage existing repositories (list & delete).

### 💼 Job Email Generator
- Upload a **PDF/DOCX resume** or paste your resume text.
- Sanitize personal data (email, phone numbers).
- Paste or upload a **Job Description (JD)**.
- Generate a professional email using **Gemma**.
- Edit, review, and send the generated email via Gmail.
- Log all sent emails in a local folder.

---

## 🧱 Project Structure

```
codepush-agent/
├── app.py                # Main Streamlit application
├── github_agent.py       # Handles GitHub operations
├── gemma_agent.py        # Generates email content via Gemma
├── gmail_sender.py       # Sends emails via Gmail
├── requirements.txt      # Dependencies (recommended)
├── .env                  # Environment variables (ignored in Git)
└── README.md             # This file
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/codepush-agent.git
cd codepush-agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```bash
GITHUB_TOKEN=ghp_xxx...
GMAIL_ADDRESS=you@example.com
APP_LOG_DIR=logs
GEMINI_API_KEY=AIza...
```

---

## 🧩 Usage

Run the app locally:
```bash
streamlit run app.py
```

Then open the displayed URL, usually [http://localhost:8501](http://localhost:8501)

### 🔹 Tab 1: Code Deployer
1. Enter GitHub repo name, branch, and commit message.
2. Upload files or a zipped project folder.
3. Optionally auto-generate a README.md.
4. Click **Push to GitHub**.
5. View upload status and logs.

### 🔹 Tab 2: Job Email Generator
1. Paste or upload your resume.
2. Paste the job description.
3. Click **Generate Email** (Gemma-powered).
4. Edit and review the AI-generated email.
5. Enter recipient and your Gmail, then send.
6. A copy of each sent email is saved in the `logs/` folder.

---

## 🧰 Security & Git Hygiene

Create a `.gitignore` file:
```bash
.env
token.json
token.pickle
credentials.json
venv/
logs/
__pycache__/
```

---

## 🪶 License
MIT License © 2025 Dinesh Karri

---
