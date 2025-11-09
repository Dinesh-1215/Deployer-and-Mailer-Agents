Flask Resume Analyzer

A lightweight Flask-based Resume Analyzer that compares a candidate’s resume with a provided Job Description (JD) to compute an ATS (Applicant Tracking System) Score and generate improvement suggestions using Gemini/Gemma or TF-IDF fallback models.

⸻

🚀 Features
	•	Resume input: Upload PDF/DOCX/TXT or paste plain text.
	•	Job Description input: Paste text or provide a public JD URL.
	•	Keyword & Semantic Scoring: Combines keyword match (TF-IDF) and semantic similarity (Gemini embeddings or TF-IDF fallback).
	•	Gemma-powered Suggestions: Suggests improved resume bullet points based on JD context.
	•	Logging: Detailed console logs for traceability (embedding creation, file extraction, scoring, etc.).
	•	Temporary file handling: Uploaded files are deleted immediately after processing.

⸻

🧠 Tech Stack
	•	Flask (backend web framework)
	•	pdfplumber, python-docx (text extraction)
	•	scikit-learn (TF-IDF and similarity metrics)
	•	Google GenAI SDK (google.genai) (optional, for embeddings and suggestions)
	•	Bootstrap 5 (UI styling)

⸻

📂 Project Structure

Flask-Resume-Analyzer/
│
├── app.py                # Main Flask application
├── README.md             # Documentation
├── requirements.txt      # Python dependencies
└── templates/ (optional) # If you split HTML out later


⸻

⚙️ Installation

1. Clone the Repository

git clone https://github.com/<your-username>/Flask-Resume-Analyzer.git
cd Flask-Resume-Analyzer

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3. Install Dependencies

pip install -r requirements.txt

4. (Optional) Set Up Environment Variables

Create a .env file and add:

FLASK_SECRET=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key_here


⸻

🧩 Usage

Run the Flask Server

python app.py

Access the web interface at: http://127.0.0.1:5000￼

Steps
	1.	Upload or paste your Resume (left panel)
	2.	Paste or provide a Job Description URL (right panel)
	3.	Click Analyze
	4.	View:
	•	ATS Score (Keyword + Semantic)
	•	Matched & Missing Keywords
	•	Gemma-based Resume Suggestions

⸻

🧾 Example Output

ATS Score: 85.3%
Keyword Match: 72.4%
Semantic Match: 89.1% (via TF-IDF)

Present Keywords: ['python', 'ai', 'ml', 'flask', 'data']
Missing Keywords: ['deployment', 'cloud', 'nlp']

Suggestions:
- Optimized model training pipelines using Python and TensorFlow.
- Automated document parsing with Flask and pdfplumber.
- Designed scalable AI workflows improving inference time by 25%.


⸻

🧰 Requirements

Flask
pdfplumber
python-docx
scikit-learn
numpy
requests
python-dotenv
google-genai  # optional

Install via:

pip install -r requirements.txt


⸻

🐳 Docker (Optional)

FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]

Build & Run:

docker build -t resume-analyzer .
docker run -p 5000:5000 resume-analyzer


⸻

⚖️ License

MIT License — free for personal and commercial use.

⸻

💬 Contact

Author: Dinesh Karri
Email: [email hidden for privacy]
GitHub: https://github.com/Dinesh-1215￼

⸻

🚀 “Analyze. Improve. Impress.” — Smart resume optimization powered by Generative AI.