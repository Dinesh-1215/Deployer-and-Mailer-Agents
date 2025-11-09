import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_email_with_attachment(subject, body, to_email, resume_file, from_email):
    service = get_gmail_service()

    message = MIMEMultipart()
    message['to'] = to_email
    message['from'] = from_email
    message['subject'] = subject

    # Add plain text message
    msg = MIMEText(body, 'plain')
    message.attach(msg)

    # Attach resume if provided
    if resume_file is not None:
        resume_file.seek(0)
        resume_data = resume_file.read()
        filename = resume_file.name

        part = MIMEApplication(resume_data, Name=filename)
        part['Content-Disposition'] = f'attachment; filename=\"{filename}\"'
        message.attach(part)

    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_message = {'raw': raw_message}

    sent = service.users().messages().send(userId='me', body=send_message).execute()
    return sent