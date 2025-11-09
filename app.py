import streamlit as st
import os
import tempfile
import datetime
import fitz  # PyMuPDF
from docx import Document
import re
from dotenv import load_dotenv
from github_agent import (
    push_folder_to_github,
    list_github_repos,
    delete_github_repo
)
from gemma_agent import generate_email_with_gemma
from gmail_sender import send_email_with_attachment
import zipfile
import io

# Load environment
load_dotenv()
DEFAULT_GMAIL = os.getenv("GMAIL_ADDRESS", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LOG_DIR = os.getenv("APP_LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

st.set_page_config(page_title="Code Deployer & Mail Agent", page_icon="🤖")
st.title("🤖 Code Deployer & Mail Agent")

# Helpers

def log(msg: str):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[LOG] {ts} - {msg}")


def is_valid_repo_name(name: str) -> bool:
    return bool(re.match(r'^[A-Za-z0-9_.-]{1,100}$', name))


# Tabs
tab1, tab2 = st.tabs(["🚀 Code Deployer", "💼 Email Generator"])

# ---------------------- Tab 1: Code Deployer ----------------------
with tab1:
    st.header("📄 Push Local Folder to GitHub")

    repo_name = st.text_input("🔧 GitHub Repository Name")
    branch = st.text_input("🌿 Branch Name", value="main")
    commit_message = st.text_input("📝 Commit Message", value="Add folder contents")

    st.markdown("**You can upload multiple files or a zipped folder.**")
    uploaded_files = st.file_uploader("📁 Upload files", type=None, accept_multiple_files=True)
    uploaded_zip = st.file_uploader("🗜️ Or upload a zipped folder (.zip)", type=["zip"], accept_multiple_files=False)

    generate_readme = st.checkbox("📄 Generate README.md", value=True)
    readme_text = ""
    if generate_readme:
        readme_text = st.text_area("📝 README.md Content", "## Project Title\n\nDescription goes here.")

    # Show GH token warning if not set
    if not GITHUB_TOKEN:
        st.warning("GITHUB_TOKEN not set. Push to GitHub will likely fail until you set it in your environment or .env file.")

    def _save_uploaded_files_to_dir(tmpdir: str):
        # returns list of saved file paths
        saved = []
        # Save individual files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                safe_name = os.path.basename(uploaded_file.name)
                file_path = os.path.join(tmpdir, safe_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())
                saved.append(file_path)
        # Extract zip if uploaded
        if uploaded_zip:
            zip_path = os.path.join(tmpdir, os.path.basename(uploaded_zip.name))
            with open(zip_path, "wb") as f:
                f.write(uploaded_zip.read())
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(tmpdir)
            # collect extracted files (flat)
            for root, _, files in os.walk(tmpdir):
                for fn in files:
                    saved.append(os.path.join(root, fn))
        return saved

    push_btn = st.button("🚀 Push to GitHub")
    if push_btn:
        if (not uploaded_files and not uploaded_zip) or not repo_name:
            st.error("Please upload files or a zip, and provide repository name.")
        elif not is_valid_repo_name(repo_name):
            st.error("Repository name contains invalid characters. Use letters, numbers, -, _, or .")
        else:
            with tempfile.TemporaryDirectory() as tmpdirname:
                saved_files = _save_uploaded_files_to_dir(tmpdirname)

                # Add README if requested
                if generate_readme:
                    readme_path = os.path.join(tmpdirname, "README.md")
                    with open(readme_path, "w", encoding='utf-8') as f:
                        f.write(readme_text)
                    saved_files.append(readme_path)

                if not saved_files:
                    st.error("No files found to push after extraction.")
                else:
                    with st.spinner("Pushing files to GitHub..."):
                        try:
                            results = push_folder_to_github(repo_name, tmpdirname, branch, commit_message)
                        except Exception as e:
                            st.error(f"Failed to push to GitHub: {e}")
                            log(f"push_folder_to_github exception: {e}")
                            results = None

                    if not results:
                        st.error("No response from push action. Check logs or credentials.")
                    else:
                        # results expected as iterable of (file, status, resp)
                        success_count = 0
                        fail_count = 0
                        rows = []
                        for file, status, resp in results:
                            if status in (200, 201):
                                success_count += 1
                                rows.append((file, 'OK'))
                            else:
                                fail_count += 1
                                msg = resp.get('message') if isinstance(resp, dict) else str(resp)
                                rows.append((file, f'ERR: {msg}'))

                        st.write(f"✅ Success: {success_count}, ❌ Failed: {fail_count}")
                        st.table(rows)

    st.markdown("---")
    st.header("🗂️ Manage Your Repositories")

    # Load repo list once
    if "repos" not in st.session_state:
        try:
            st.session_state["repos"] = list_github_repos()
        except Exception as e:
            st.session_state["repos"] = []
            log(f"list_github_repos failed: {e}")

    repos = st.session_state.get("repos", [])

    if "selected_repos" not in st.session_state:
        st.session_state.selected_repos = []

    st.subheader("📚 Select repositories to delete:")
    for repo in repos:
        key = f"delete_{repo}"
        checked = st.checkbox(repo, key=key)
        if checked and repo not in st.session_state.selected_repos:
            st.session_state.selected_repos.append(repo)
        if not checked and repo in st.session_state.selected_repos:
            st.session_state.selected_repos.remove(repo)

    selected_repos = list(st.session_state.selected_repos)

    if selected_repos:
        st.warning(f"⚠️ You have selected {len(selected_repos)} repository(ies) for deletion.")
        confirm = st.checkbox("✅ Confirm permanent deletion of selected repositories")
        if st.button("🗑️ Delete Selected Repositories"):
            if confirm:
                for repo in selected_repos:
                    try:
                        success = delete_github_repo(repo)
                    except Exception as e:
                        success = False
                        log(f"delete_github_repo failed for {repo}: {e}")
                    if success:
                        st.success(f"✅ Deleted: {repo}")
                    else:
                        st.error(f"❌ Failed to delete: {repo}")
                # refresh
                try:
                    st.session_state["repos"] = list_github_repos()
                except Exception as e:
                    st.session_state["repos"] = []
                    log(f"list_github_repos failed after deletion: {e}")
                st.session_state.selected_repos = []
            else:
                st.warning("Please confirm the deletion.")
    else:
        st.info("No repositories selected.")

# ---------------------- Tab 2: Job Email Generator ----------------------
with tab2:
    st.header("📧 AI-Powered Job Email Generator")

    job_description = st.text_area("📝 Paste the Job Description", height=200)
    uploaded_resume = st.file_uploader("📌 Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"]) 

    resume_text = ""
    if uploaded_resume:
        try:
            data = uploaded_resume.read()
            bio = io.BytesIO(data)
            if uploaded_resume.name.lower().endswith(".pdf"):
                # fitz expects bytes for stream
                bio.seek(0)
                with fitz.open(stream=bio.read(), filetype="pdf") as doc:
                    resume_text = "\n".join(page.get_text() for page in doc)
            else:
                bio.seek(0)
                doc = Document(bio)
                resume_text = "\n".join([p.text for p in doc.paragraphs])

            # Sanitize personal data with safer regex
            resume_text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[email hidden]", resume_text)
            resume_text = re.sub(r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?(?:\(\d{2,4}\)|\d{2,4})[-.\s]?\d{3,4}[-.\s]?\d{3,4}(?!\w)", "[phone hidden]", resume_text)
        except Exception as e:
            st.error(f"❌ Failed to extract resume text: {e}")
            log(f"resume extraction failed: {e}")

    if resume_text:
        st.markdown("### 🔍 Preview Sanitized Resume")
        st.text_area("Sanitized Resume Text", resume_text, height=200)

    your_skills = st.text_area("🧠 Paste Your Skills or Work Experience", value=resume_text, height=150)
    extra_notes = st.text_area("💡 Optional: Add Extra Instructions for Email Tone or Content")
    humanize = st.checkbox("🤖 Make the email sound more human", value=True)

    generate_btn = st.button("📩 Generate Email with Gemma")
    regenerate_btn = st.button("♻️ Regenerate with New Instructions")

    if generate_btn or regenerate_btn:
        if job_description and your_skills:
            with st.spinner("🧠 Thinking..."):
                try:
                    # Build prompt wrapper in agent
                    email = generate_email_with_gemma(job_description, your_skills + ' ' + (extra_notes or ''))
                    if email:
                        # remove markdown artifacts
                        email = email.replace("**", "").replace("__", "")
                        st.session_state["generated_email"] = email
                        st.success("Email generated — review below.")
                    else:
                        st.error("Gemma returned empty response.")
                except Exception as e:
                    st.error(f"Gemma generation failed: {e}")
                    log(f"Gemma generation error: {e}")
        else:
            st.error("Please provide both job description and your skills.")

    if "generated_email" in st.session_state:
        st.subheader("✍️ Review and Edit Your Email")

        subject = st.text_input("📜 Subject", value=st.session_state.get("generated_subject", "Job Application"))
        edited_email = st.text_area("📨 Your Email Content", value=st.session_state["generated_email"], height=300)

        st.markdown("### 📤 Send Your Email")
        to_email = st.text_input("📧 Recipient Email", placeholder="recruiter@company.com")
        your_email = st.text_input("📩 Your Gmail Address (sender)", value=DEFAULT_GMAIL)

        if st.button("✅ Send Email via Gmail"):
            if not to_email or not your_email:
                st.warning("Please enter both sender and recipient email addresses.")
            else:
                try:
                    with st.spinner("📁 Sending email..."):
                        send_email_with_attachment(subject, edited_email, to_email, uploaded_resume, from_email=your_email)
                        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                        safe_name = re.sub(r'[^A-Za-z0-9_.-]', '_', f"job_email_{timestamp}.txt")
                        log_file = os.path.join(LOG_DIR, safe_name)
                        with open(log_file, "w", encoding='utf-8') as f:
                            f.write(f"To: {to_email}\nFrom: {your_email}\nSubject: {subject}\n\n{edited_email}")
                        st.success("✅ Email sent and saved to logs!")
                except Exception as e:
                    st.exception(e)
                    st.error(f"❌ Failed to send email: {e}")
