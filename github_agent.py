import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def push_file_to_github(repo_name, branch, file_path, file_content, commit_message):
    api_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # Check if file already exists
    res = requests.get(api_url, headers=headers)
    sha = res.json().get("sha") if res.status_code == 200 else None

    data = {
        "message": commit_message,
        "content": base64.b64encode(file_content).decode(),
        "branch": branch
    }

    if sha:
        data["sha"] = sha

    response = requests.put(api_url, json=data, headers=headers)
    return response.status_code, response.json()

def push_folder_to_github(repo_name, folder_path, branch="main", commit_message="Add folder contents"):
    results = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, folder_path)
            with open(abs_path, "rb") as f:
                content = f.read()
            status, resp = push_file_to_github(repo_name, branch, rel_path.replace("\\", "/"), content, commit_message)
            results.append((rel_path, status, resp))
    return results

def list_github_repos():
    url = "https://api.github.com/user/repos?per_page=100"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [repo["name"] for repo in response.json()]
    else:
        return []

def delete_github_repo(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 204