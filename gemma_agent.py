import os
import requests

GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")

def generate_email_with_gemma(job_desc, skills):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    prompt = f"""You are an expert career assistant. Write a professional job application email based on the following:

Job Description:
{job_desc}

Candidate Skills/Experience:
{skills}

Make it polite, enthusiastic, and easy to edit.
"""

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7
        }
    }

    params = {"key": GEMMA_API_KEY}
    response = requests.post(url, headers=headers, params=params, json=body)
    if response.status_code == 200:
        candidates = response.json().get("candidates", [])
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]
        else:
            return "❌ No response generated."
    else:
        return f"❌ Error: {response.status_code} - {response.text}"