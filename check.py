import requests
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
print("GITHUB_TOKEN:", GITHUB_TOKEN)  # Debugging line to check if token is loaded

GITHUB_USERNAME = "Dinesh-1215"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

response = requests.get("https://api.github.com/user", headers=headers)

if response.status_code == 200:
    print("✅ Token works! Logged in as:", response.json()["login"])
else:
    print("❌ Token failed. Status:", response.status_code)
    print("Response:", response.json())